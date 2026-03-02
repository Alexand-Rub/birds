from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey


def bird_file_directory_path(instance: "Bird", filename: str) -> str:
    return "Bird/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )

class Bird(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    lat_name = models.CharField(max_length=50, blank=True, null=True)
    squad = models.CharField(max_length=50, blank=True, null=True)
    family = models.CharField(max_length=50, blank=True, null=True)
    genus = models.CharField(max_length=50, blank=True, null=True)
    protection = models.CharField(max_length=50, blank=True, null=True)
    habitat = models.TextField(max_length=1000, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    audio = models.FileField(upload_to="songs/", blank=True, null=True)
    logo_men = models.ImageField(null=True, blank=True, upload_to=bird_file_directory_path)
    logo_woman = models.ImageField(null=True, blank=True, upload_to=bird_file_directory_path)
    favourites = models.ManyToManyField(User, related_name="favourites", blank=True)
