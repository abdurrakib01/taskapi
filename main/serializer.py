from rest_framework import serializers
from .models import Team, Task

class TeamSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ('id', 'name', 'username', 'teams')
    def get_username(self, obj):
        return [user.username for user in obj.teams.all()]

class TaskSerializer(serializers.ModelSerializer):
    assign_username = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ('title', 'des', 'due_date', 'status', 'priority', 'assign_username')
    
    def get_assign_username(self, obj):
        return [user.username for user in obj.assign.all()]