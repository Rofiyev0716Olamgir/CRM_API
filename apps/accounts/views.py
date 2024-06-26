from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .models import (
    User,
    Group,
    Worker,
    UserToken
)
from .serializers import (
    WorkerRegisterSerializer,
    UserVerifySerializer,
    ChangePasswordSerializer,
    SendMailSerializer,
    ResetPasswordSerializer,
    ProfileSerializer,
)
from .tasks import send_mail_func


class WorkerRegisterView(generics.GenericAPIView):
    serializer_class = WorkerRegisterSerializer
    queryset = Worker.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        token = UserToken.objects.create(user=user)
        send_mail_func.apply_async(('Cearem', f'Token {str(token.token)}, url: http://localhost:8000/uz/accounts/user/verify/{email}/', [user.email]), )
        data = {
            'success': True,
            'message': 'Worker successfully registered.',
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserVerifyView(generics.GenericAPIView):
    serializer_class = UserVerifySerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        context = {
            'email': kwargs.get('email'),
            'request': request
        }
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': True,
            'message': 'User successfully registered.',
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    pass


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': True,
            'message': 'User password successfully changed.',
        }
        return Response(data, status=status.HTTP_201_CREATED)


class SendMailView(generics.GenericAPIView):
    serializer_class = SendMailSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        token = UserToken.objects.create(user=user)
        send_mail_func.apply_async(('Cearem resit password', f'Token:{str(token.token)}, url: http://localhost:8000/uz/accounts/password/mail/reset/{email}/', [user.email]), )
        data = {
            'success': True,
            'message': 'Send mail url',
        }
        return Response(data, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        context = {
            'email': kwargs.get('email'),
            'request': request
        }
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'success': True,
            'message': 'User password successfully changed.',
        }
        return Response(data, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user