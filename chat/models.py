from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    date_add=models.DateTimeField(auto_now_add=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    photo=models.ImageField(upload_to="users_photo")
    dateNaissance=models.DateField()
    level=models.IntegerField(default=5)

    def __str__(self):
        return self.user.username
