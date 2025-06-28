from rest_framework import serializers
from .models import CustomUser, UserProfile
from django.conf import settings
from allauth.account.forms import ResetPasswordForm
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth import get_user_model

# --- UserProfileSerializer and UserSerializer remain the same ---
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'date_of_birth', 'verification_status']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_type', 'first_name', 'last_name', 'profile']


# --- RegisterSerializer is FIXED ---
# This serializer now correctly handles the `request` object passed by
# dj-rest-auth's RegisterView, resolving the `save()` method error.
class RegisterSerializer(serializers.ModelSerializer):
    # This is the password confirmation field dj-rest-auth expects
    re_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 're_password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8}
        }

    def validate(self, data):
        """
        Check that the two password entries match.
        """
        if data['password'] != data['re_password']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def save(self, request=None):
        """
        Explicitly define a save method that can accept the `request` object
        passed by the RegisterView.
        """
        user = CustomUser.objects.create_user(
            email=self.validated_data['email'],
            password=self.validated_data['password'],
            first_name=self.validated_data.get('first_name', ''),
            last_name=self.validated_data.get('last_name', '')
        )
        # In the future, you could use the request object here, for example:
        # user.created_from_ip = request.META.get('REMOTE_ADDR')
        # user.save()
        return user


class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    This serializer's only job is to validate the email and then trigger
    our new CustomResetPasswordForm.
    """
    password_reset_form_class = ResetPasswordForm