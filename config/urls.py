from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt
from media_tracker.views import MediaItemViewSet
from media_tracker.registration_views import register_user

# Initialize router for ViewSets
router = DefaultRouter()
router.register(r'media-items', MediaItemViewSet, basename='media-item')

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),
    
    # DRF API Endpoints
    path('api/', include(router.urls)),
    
    # Simple Registration Endpoint (no CSRF needed - uses Token Auth)
    path('api/auth/register/', register_user, name='register'),
    
    # Other Authentication Endpoints (dj-rest-auth)
    path('api/auth/', include('dj_rest_auth.urls')),
] 