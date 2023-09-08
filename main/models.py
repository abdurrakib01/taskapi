from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    name = models.CharField(max_length=50)
    teams = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Task(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    des = models.TextField(max_length=300)
    due_date = models.DateField()
    assign = models.ManyToManyField(User)
    status = models.CharField(max_length=50)
    priority = models.PositiveIntegerField()

    def __str__(self):
        return self.title