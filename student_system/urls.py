"""
URL configuration for student_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.templatetags.static import static as static_url
from django.http import JsonResponse
from . import views

urlpatterns = [
    # Favicon and Chrome DevTools endpoints (prevents 404 log noise)
    path('favicon.ico', RedirectView.as_view(url=static_url('images/favicon.ico'), permanent=True)),
    path('.well-known/appspecific/com.chrome.devtools.json', lambda request: JsonResponse({}, status=200)),
    
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # Authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    
    # API URLs
    path('api/', include('student_system.api_urls')),
    
    # App URLs
    path('students/', include('students.urls')),
    path('courses/', include('courses.urls')),
    path('enrollments/', include('enrollments.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from both STATICFILES_DIRS and STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=str(settings.BASE_DIR / 'static'))
