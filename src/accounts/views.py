from django.contrib.auth import authenticate
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserPasswordResetSerializer,UserChangePasswordSerializer,UserProfileSerializer,UserRegistrationSerializer,UserLoginSerializer,SendPasswordResetEmailSerializer

from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializers import UpdateUserSerializer

from accounts.serializers import UpdateProfilePictureSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(
        operation_description="Endpoint Login",
        request_body=UserRegistrationSerializer

    )
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token":token,"msg":"Registration successful"},status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#LOGIN
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(
        operation_description="Endpoint Login",
        request_body=UserLoginSerializer

    )
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.data.get('email')
        password = serializer.data.get('password')
        user=authenticate(email=email,password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Login Sucess'},status=status.HTTP_200_OK)

        return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Endpoint Login",
        request_body=UserChangePasswordSerializer

    )
    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':"Password changed"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(
        operation_description="Endpoint Login",
        request_body=SendPasswordResetEmailSerializer

    )
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': "Password reset link.Check Email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(
        operation_description="Changement de password",
        request_body=UserPasswordResetSerializer

    )
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data,context={'uid':uid,"token":token})
        if serializer.is_valid(raise_exception=True):
            return  Response({'msg':"Password Reset Sucessfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    @swagger_auto_schema(
        operation_description="Mise a jour profile",

        request_body=UpdateUserSerializer,



    )
    def post(self, request):
      #  user_id = request.query_params.get('param')
       # if user_id is None:
        #    return Response({"error": "Missing 'param' parameter in the request"}, status=status.HTTP_400_BAD_REQUEST)
        # code for handling the GET request with the 'param'
        user = request.user
        if user is None:
            return Response({"error": "Assurez voud d'etre connecté"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfilePictureView(APIView):
    @swagger_auto_schema(
        operation_description="Update Profile",
        request_body=UpdateProfilePictureSerializer

    )
    def post(self, request):
        user = request.user
        serializer = UpdateProfilePictureSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Profile picture updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)