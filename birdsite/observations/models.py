from django.db import models
from django.contrib.auth.models import User

from birdlib.models import Bird


class Observations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField()
    region = models.CharField(max_length=200, null=False)
    reconciliation = models.TextField(max_length=1000, null=False)
    image = models.ImageField(upload_to='images/observations/', null=True, blank=True)
    gender = models.CharField(max_length=200, null=False)
