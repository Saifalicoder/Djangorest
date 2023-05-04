from django.contrib import admin
from django.urls import path, include
from . import views
from .views import signup
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('',  views.getRoutes),
    path('user/', views.getUsers),
    path('signup/', signup, name='signup'),
    path('books/', views.getBooks),
    path('book/<str:pk>', views.getBook),
    path('user/<str:pk>/', views.getUser),
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
