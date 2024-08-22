"""
URL configuration for nashhappsapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from nashhappsapi.views.localnash import TheLocalEventViewSet
from nashhappsapi.views.events import FetchEventsViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'localevents', TheLocalEventViewSet, 'localevent')
router.register(r'fetch_events', FetchEventsViewSet, basename='fetch_events')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Django Allauth URLs
]