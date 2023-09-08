from django.shortcuts import render
from rest_framework import generics
from .serializer import TeamSerializer, TaskSerializer
from rest_framework.views import APIView
from .models import Team, Task
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.

class TeamView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        queryset = Team.objects.filter(Q(author=request.user) | Q(teams=request.user))
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)