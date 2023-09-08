from django.contrib import admin
from .models import Team, Task
# Register your models here.

class CustomTeam(admin.ModelAdmin):
    list_display = ['id', 'name']
admin.site.register(Team, CustomTeam)
admin.site.register(Task)
