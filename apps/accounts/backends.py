from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneNumberBackend(BaseBackend):
    """
    Authenticate users using phone number and password.
    """

    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        if phone_number is None or password is None:
            return None

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        return user.is_active