from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Color(models.Model):
    """ Store all available colors here """
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
