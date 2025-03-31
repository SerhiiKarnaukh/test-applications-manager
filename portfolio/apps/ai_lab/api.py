from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from openai import OpenAI

from core.utils import print_object


class AiLabTestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        question = request.data.get("question")
        api_key = settings.OPENAI_API_KEY
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Answer briefly and in the form of a joke"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": question
                        }
                    ]
                },
            ],)

        print_object(response)

        return Response({"message": response.output_text})
