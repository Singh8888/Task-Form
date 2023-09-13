from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.generics import GenericAPIView ,ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from formApp.renders import UserRenderer
import random
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import  render,redirect
from django.http import JsonResponse
from rest_framework import filters



class RegisterUserAPIView(GenericAPIView):
    renderer_classes = [UserRenderer]
    def get(self,request):
        return Response()
    def post(self,request,format=None):
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                print("it is woriking")
                user = serializer.save()
                return Response({'msg':'Registration successfull'},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
      
      
class LoginUserAPIView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email,password=password)
        if user is not None and user.is_active:
            token= Token.get_token(user)
            return Response({'msg':'user has been login successfully','token':token},status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email and password are not valid']}},status=status.HTTP_404_NOT_FOUND)
    

def registration(request):
    return render(request,'registration.html')

  
def login(request):
    return render(request,'login.html')
