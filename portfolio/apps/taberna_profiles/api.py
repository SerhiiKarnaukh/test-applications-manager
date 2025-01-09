from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView


from .models import UserProfile
from accounts.models import Account
from taberna_orders.models import Order

from accounts.serializers import ProfileCreateSerializer
from taberna_orders.serializers import OrderSerializer

from accounts.utils import send_activation_email


class TabernaProfileCreateView(generics.CreateAPIView):
    serializer_class = ProfileCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            user_id = response.data.get('id')
            existing_user = Account.objects.get(id=user_id)

            # send activation email
            send_activation_email(existing_user, request)

            self.create_profile(existing_user)

            return response

        except Exception as e:

            error_message = str(e)
            if 'unique' in error_message and 'email' in error_message:
                email = self.request.data.get('email')
                existing_user = Account.objects.filter(email=email).first()
                if existing_user:
                    if not hasattr(existing_user, 'userprofile'):
                        self.create_profile(existing_user)
                        return Response({"detail": "taberna_profile_created"},
                                        status=status.HTTP_200_OK)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)

    def create_profile(self, user):
        UserProfile.objects.create(user=user)


class UserOrdersListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.userprofile, is_ordered=True).order_by("-created_at")
