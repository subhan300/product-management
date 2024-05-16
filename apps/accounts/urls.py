# urls.py

from django.urls import path
from .views import ProfileView, UserLoginView, ForgotPasswordView, LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forget-password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:key>/', ProfileView.as_view(), name='change_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('password_reset_confirm/', LogoutView.as_view(), name='password_reset_confirm'),
]
