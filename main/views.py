from django.shortcuts import render
from rest_framework import generics
from .serializer import TeamSerializer, TaskSerializer
from rest_framework.views import APIView
from .models import Team, Task
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
# Create your views here.

class TeamView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        queryset = Team.objects.filter(Q(author=request.user) | Q(teams=request.user)).distinct()
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        queryset = Task.objects.filter(team=pk)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk, format=None):
        team = Team.objects.get(pk=pk)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(team=team)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, pk, format=None):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(status=status.HTTP_200_OK)
