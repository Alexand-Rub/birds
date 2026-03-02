from django.contrib.auth.models import User
from django.db import models

class Discussions(models.Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField(max_length=1000, null=False)
    image = models.ImageField(upload_to='images/discussions/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

class Message(models.Model):
    text = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussions, on_delete=models.CASCADE)
