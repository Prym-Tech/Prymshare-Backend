from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
# --- CHANGE START ---
from rest_framework_nested import routers
from pages.views import PageViewSet
from storefront.views import ProductViewSet
# --- CHANGE END ---

# --- CHANGE START ---
# We use a nested router to create the /pages/{id}/products/ endpoint
router = routers.SimpleRouter()
router.register(r'pages', PageViewSet, basename='page')

pages_router = routers.NestedSimpleRouter(router, r'pages', lookup='page')
pages_router.register(r'products', ProductViewSet, basename='page-products')
# --- CHANGE END ---


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- CHANGE START ---
    # The new router handles the pages and nested product URLs
    path('api/', include(router.urls)),
    path('api/', include(pages_router.urls)),
    # --- CHANGE END ---

    # API endpoints for your apps
    path('api/', include('pages.urls')),
    path('api/images/', include('images.urls')),
    # path('api/', include('storefront.urls')), # This line is now handled by the nested router above

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