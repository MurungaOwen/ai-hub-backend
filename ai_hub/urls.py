"""
URL configuration for ai_hub project.
"""
from django.contrib import admin
from django.urls import path, include
from .config import schema_view
from django.conf import settings
from django.conf.urls.static import static
from lesson.user_view import register_user, login_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/auth/register', register_user),
    path('api/v1/auth/login', login_user),
    path('api/v1/community/', include('forums.urls')),
    path('api/v1/payment/', include('payment.urls')),
    path('api/v1/', include('lesson.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
