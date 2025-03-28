from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from openai import OpenAI


class AiLabTestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        question = request.data.get("question")
        api_key = settings.OPENAI_API_KEY
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": question
            }]
        )

        return Response({"message": completion.choices[0].message.content})
