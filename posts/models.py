from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField()
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.time)
