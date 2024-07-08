from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

def validate_email(value):
    email = User.objects.filter(email__iexact = value)
    if email.exists():
        raise serializers.ValidationError('Email must be unique')
    return value