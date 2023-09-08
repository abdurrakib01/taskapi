from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserRegistrationSerializer, UserLoginSerializer, UserInfoSerializer, UserListSerializer
from rest_framework import status
from .models import UserInfo
from rest_framework.authentication import authenticate
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            UserInfo.objects.create(user=user)
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msg':'Login Successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'non_field_errors':['username or password is not valid']},
                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user_info = UserInfo.objects.get(user=request.user)
        serializer = UserInfoSerializer(user_info, context={'request':request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        userinfo = UserInfo.objects.get(user=request.user)
        serializer = UserInfoSerializer(userinfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, format=None):
        userinfo = UserInfo.objects.get(user=request.user)
        data = request.data 
        userinfo.image = data.get('image', userinfo.image)
        userinfo.bio = data.get('bio', userinfo.bio)
        userinfo.save()
        serializer = UserInfoSerializer(userinfo)
        return Response(serializer.data)
    
    def delete(self, request, format=None):
        userinfo = UserInfo.objects.get(user=request.user)
        userinfo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_userlist(request):
    users = User.objects.all()
    user = users.exclude(id=request.user.id)
    serializer = UserListSerializer(user, many=True)
    return Response(serializer.data)