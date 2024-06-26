from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers


from .models import User, Group, Worker, UserToken


class WorkerRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Worker
        fields = ['email', 'position']


class UserVerifySerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, validators=[validate_password])
    token = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ('token', 'password1', 'password2')

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        token = attrs.get('token')
        email = self.context.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if password1 == password2:
                if UserToken.objects.filter(user=user).exists():
                    token_last = UserToken.objects.filter(user=user).last()
                    if token_last.token == token:
                        user.is_active = True
                        user.is_user_active = True
                        UserToken.objects.get(token=token_last.token).is_used = True
                        user.save()
                    raise ValidationError('The token did not match')
                raise ValidationError('Token already exists')
            raise ValidationError('Passwords do not match')
        raise ValidationError('Email already registered')

    def create(self, validated_data):
        email = self.context.get('email')
        password = validated_data.pop('password1')
        user = get_object_or_404(User, email=email)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True,)
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        fields = ('old_password', 'password1', 'password2')

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        password = attrs.get('password')
        if self.context['request'].user.check_password(password):
            if password != password1:
                if password1 == password2:
                    return attrs
                raise ValidationError('Passwords do not match')
            raise ValidationError('Passwords do not match')
        raise ValidationError('Old passwords do not match')

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        user = self.context['request'].user
        user.set_password(password1)
        user.save()
        return user


class SendMailSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            return attrs
        raise ValidationError('Email already registered')


class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, validators=[validate_password])
    token = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ('token', 'password1', 'password2')

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        token = attrs.get('token')
        email = self.context.get('email')
        if User.objects.filter(email=email).exists():
            user = get_object_or_404(User, email=email)
            if password1 == password2:
                if UserToken.objects.filter(user=user).exists():
                    token_last = UserToken.objects.filter(user=user).last()
                    if token_last.token == token:
                        UserToken.objects.get(token=token_last.token).is_used = True
                        return attrs
                    raise ValidationError('The token is invalid')
                raise ValidationError('Token already exists')
            raise ValidationError('Passwords do not match')
        raise ValidationError('Email already registered')

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        email = self.context.get('email')
        user = get_object_or_404(User, email=email)
        user.set_password(password1)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'avatar', 'phone', 'is_active', 'is_user_active',
                  'is_staff', 'is_superuser', 'modified_date', 'created_date')
        red_only_fields = ['email', 'is_active', 'is_user_active', 'is_staff', 'is_superuser', 'modified_date', 'created_date']


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'first_name', 'last_name']

