from django.shortcuts import render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

# (Keep your other imports and views if they exist in this file)

class GoogleLogin(SocialLoginView):
    """
    This view handles the Google login process. It takes the access token from
    the frontend, verifies it with Google, and then logs in or creates a
uperuser
    user in our system, returning our app's JWT.
    """
    adapter_class = GoogleOAuth2Adapter
    # The callback URL is not strictly necessary for this API-only flow, but it's
    # good practice to have it match what's in your Google Cloud console.
    callback_url = 'http://localhost:5173' 
    client_class = OAuth2Client
