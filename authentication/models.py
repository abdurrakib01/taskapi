from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pic', default='./static/images/profile.jpeg')
    bio = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username