from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True,       null=True)
    objects = models.Manager()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.title
