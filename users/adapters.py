from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        # print('get-confirm')
        """
        Constructs the final frontend URL for account activation.
        This must match the route in your React application.
        """
        # The key is the unique token for the email confirmation.
        key = emailconfirmation.key
        # Construct the full URL for the frontend.
        return f"{settings.FRONTEND_URL}/activate/{key}"

    