import os
import requests
import uuid
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .tools import TOOLS

from .utils import StockAPI


class OpenAIService:
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def get_ai_response(self, messages, tools):
        response = self.client.responses.create(
            model="gpt-4o", input=messages, tools=tools
        )
        return response.output[0]

    def get_img_gen_response(self, prompt):
        response = self.client.images.generate(
            model="dall-e-3", prompt=prompt,
        )
        return response.data[0].url


class AiLabChatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        question = request.data.get("question")
        openai_service = OpenAIService()
        available_functions = {"get_stock_price": StockAPI.get_stock_price}

        messages = [
            {"role": "system", "content": "Answer briefly and in the form of a joke"},
            {"role": "user", "content": question},
        ]

        response_output = openai_service.get_ai_response(messages, TOOLS)

        if response_output.type == "function_call":
            function_name = response_output.name
            function_args = json.loads(response_output.arguments)
            function_response = available_functions[function_name](**function_args)
            messages.append(response_output)
            tool_response_message = {
                "type": "function_call_output",
                "call_id": response_output.call_id,
                "output": json.dumps(function_response),
            }
            messages.append(tool_response_message)

            second_response = openai_service.get_ai_response(messages, TOOLS)

            return Response({"message": second_response.content[0].text})

        return Response({"message": response_output.content[0].text})


class AiLabImageGeneratorView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        prompt = request.data.get("question")
        if not prompt:
            return Response({"error": "Prompt is required."}, status=400)

        try:
            image_url = self.generate_image(prompt)
            full_url = self.download_and_save_image(image_url, request)

            return Response({"message": full_url})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def generate_image(self, prompt):
        openai_service = OpenAIService()
        return openai_service.get_img_gen_response(prompt)

    def download_and_save_image(self, image_url, request):
        img_response = requests.get(image_url, stream=True)
        if img_response.status_code != 200:
            raise Exception("Failed to download image.")

        content_type = img_response.headers.get("Content-Type")
        if not content_type or not content_type.startswith("image/"):
            raise Exception("URL does not point to an image.")

        filename = f"{uuid.uuid4().hex}.png"
        generated_images_dir = os.path.join(settings.MEDIA_ROOT, "generated_images")
        os.makedirs(generated_images_dir, exist_ok=True)

        filepath = os.path.join(generated_images_dir, filename)
        with open(filepath, "wb") as f:
            for chunk in img_response.iter_content(1024):
                f.write(chunk)

        media_url = os.path.join(settings.MEDIA_URL, "generated_images", filename)
        full_url = request.build_absolute_uri(media_url)
        return full_url
