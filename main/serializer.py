from rest_framework import serializers
from .models import Team, Task

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'teams')

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'des', 'due_date', 'status', 'priority', 'assign')