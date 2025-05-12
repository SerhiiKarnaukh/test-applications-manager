from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.urls import reverse


class AiLabChatViewTest(TestCase):
    @patch("ai_lab.api.OpenAIService")
    def test_text_only_request_success(self, mock_service_class):
        mock_service = MagicMock()
        mock_response = MagicMock()
        mock_response.type = "text"
        mock_response.content = [MagicMock(text="Funny AI joke")]
        mock_service.get_ai_response.return_value = mock_response
        mock_service_class.return_value = mock_service

        response = self.client.post(reverse("ai_lab:ai_lab_api"), {
            "question": "Tell me a joke."
        }, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Funny AI joke", response.data["message"])

    @patch("ai_lab.api.OpenAIService")
    @patch("ai_lab.api.StockAPI.get_stock_price")
    def test_function_call_and_follow_up_success(self, mock_stock, mock_service_class):
        mock_service = MagicMock()
        function_call_response = MagicMock()
        function_call_response.type = "function_call"
        function_call_response.name = "get_stock_price"
        function_call_response.arguments = '{"symbol": "AAPL"}'
        function_call_response.call_id = "abc123"

        follow_up_response = MagicMock()
        follow_up_response.type = "text"
        follow_up_response.content = [MagicMock(text="Stock joke")]

        mock_service.get_ai_response.side_effect = [
            function_call_response, follow_up_response
        ]
        mock_service_class.return_value = mock_service
        mock_stock.return_value = {"price": 123}

        response = self.client.post(reverse("ai_lab:ai_lab_api"), {
            "question": "What is AAPL price?"
        }, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Stock joke", response.data["message"])

    @patch("ai_lab.api.OpenAIService")
    def test_service_error_returns_500(self, mock_service_class):
        mock_service = MagicMock()
        mock_service.get_ai_response.side_effect = Exception("OpenAI down")
        mock_service_class.return_value = mock_service

        response = self.client.post(reverse("ai_lab:ai_lab_api"), {
            "question": "Something"
        }, content_type="application/json")

        self.assertEqual(response.status_code, 500)
        self.assertIn("OpenAI down", response.data["message"])

    @patch("ai_lab.api.OpenAIService")
    def test_image_prompt_included_in_user_content(self, mock_service_class):
        mock_service = MagicMock()
        mock_response = MagicMock()
        mock_response.type = "text"
        mock_response.content = [MagicMock(text="Image-based joke")]
        mock_service.get_ai_response.return_value = mock_response
        mock_service_class.return_value = mock_service

        image_urls = ["http://example.com/image1.png", "http://example.com/image2.png"]

        response = self.client.post(reverse("ai_lab:ai_lab_api"), {
            "question": "Make a joke about these images.",
            "prompt_images": image_urls
        }, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Image-based joke", response.data["message"])

        call_args = mock_service.get_ai_response.call_args[0][0]  # messages list
        user_msg = call_args[1]  # {"role": "user", "content": [...]}
        content_list = user_msg["content"]

        self.assertIn({"type": "input_text", "text": "Make a joke about these images."}, content_list)
        self.assertIn({
            "type": "input_image",
            "image_url": "http://example.com/image1.png",
            "detail": "low"
        }, content_list)
        self.assertIn({
            "type": "input_image",
            "image_url": "http://example.com/image2.png",
            "detail": "low"
        }, content_list)
