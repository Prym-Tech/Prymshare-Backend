from django.urls import path
from .views import GoogleLogin

urlpatterns = [
    # This creates a dedicated endpoint at /api/auth/google/
    path('google/', GoogleLogin.as_view(), name='google_login'),
]
