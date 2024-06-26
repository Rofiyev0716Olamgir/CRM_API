from django.shortcuts import get_object_or_404
from apps.accounts.models import User, Worker
from rest_framework import serializers
from rest_framework.exceptions import ValidationError