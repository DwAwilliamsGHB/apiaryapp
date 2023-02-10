from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=250)

class Hive(models.Model):
    title = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'hive_id': self.id})

class Comment(models.Model):
    date = models.DateField('comment date')
    content = models.TextField(max_length=250)

    hive = models.ForeignKey(
        Hive,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.date}"

