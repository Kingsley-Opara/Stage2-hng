from rest_framework import serializers
from django.contrib.auth import get_user_model
from .validators import validate_email
from userauth_org.models import Organizations

User = get_user_model()

class UserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(validators = [validate_email])
    password = serializers.CharField(write_only = True)


    class Meta:
        model = User
        fields = ['userId', 'firstname', 'lastname', 'phone', 'email', 'password']

class OrganizationSerializers(serializers.ModelSerializer):
    user = serializers.CharField(write_only = True, required= False)
    class Meta:
        model = Organizations
        fields = ['user', 'orgId', 'name', 'description']