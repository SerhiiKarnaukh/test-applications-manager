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


class AiLabTestView(APIView):
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
