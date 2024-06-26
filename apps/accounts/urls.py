from django.urls import path, include

from .views import (
    WorkerRegisterView,
    UserVerifyView,
    LoginView,
    ChangePasswordView,
    SendMailView,
    ResetPasswordView,
    ProfileView,
)


app_name = 'accounts'

urlpatterns = [
    path('user/verify/<str:email>/', UserVerifyView.as_view(), name='user-verify'),
    path('user/login/', LoginView.as_view(), name='user-login'),
    path('user/password/change/', ChangePasswordView.as_view(), name='password-change'),
    path('user/password/mail/send', SendMailView.as_view(), name='password-send'),
    path('user/password/mail/reset/<str:email>/', ResetPasswordView.as_view(), name='password-reset'),
    path('user/profile/', ProfileView.as_view(), name='profile'),
]