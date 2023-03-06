from django.urls import path
from django.urls.conf import include
from rest_framework import permissions

urlpatterns = [
    path('store/', include('store.urls')),
]