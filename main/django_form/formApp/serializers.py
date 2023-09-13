from rest_framework import serializers
from django.contrib.auth.models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str , force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode ,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
        
    
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=10,write_only=True)
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','password','confirm_password')
        extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True},
        'password': {'required': True},
        # 'username': {'required': True},
        }
    def validate(self, attrs):
       
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        try:
            if validated_data.get('email'):
                validated_data['email']=validated_data.get('email').lower()
                user = User.objects.create(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                # username=validated_data['username']
                )
                user.set_password(validated_data['password'])
                user.save()
                return user
        except:
            raise serializers.ValidationError('invalid input')


class Token(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        user.refresh_token = str(token)
        user.save()
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }