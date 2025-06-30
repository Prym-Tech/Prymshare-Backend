# prymshare_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints for your apps
    path('api/', include('pages.urls')),
    path('api/images/', include('images.urls')),
    # path('api/', include('storefront.urls')), # Uncomment when you create storefront.urls

    # Authentication endpoints from dj-rest-auth
    # This will provide endpoints like /api/auth/login/, /api/auth/logout/, /api/auth/registration/
    # and /api/auth/google/ for the Google login flow.
    path('api/social/auth/', include('allauth.urls')),

    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    path(
        'password/reset/confirm/<uidb64>/<token>/',
        TemplateView.as_view(),
        name='password_reset_confirm'
    ),
    
    path('api/google/auth/', include('users.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)