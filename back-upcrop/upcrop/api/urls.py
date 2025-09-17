from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_api, name='test_api'),
    path('auth/', views.auth_view, name='auth'),
    path('verify-token/', views.verify_token, name='verify_token'),
]