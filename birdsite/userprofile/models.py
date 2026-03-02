from django.contrib.auth.models import User
from django.db import models

def product_preview_directory_path(instance: "Profile", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)



