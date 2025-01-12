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

class Rooms(models.Model):
    date_add=models.DateTimeField(auto_now_add=True)
    online=models.IntegerField(default=0)
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Message(models.Model):
    date_add=models.DateTimeField(auto_now_add=True)
    auteur=models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user_messages")
    room=models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name="room_messages", null=True, blank=True)
    message=models.TextField()

    def __str__(self):
        return self.auteur.user.username


