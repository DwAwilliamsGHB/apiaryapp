import os
import geocoder
from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
mapbox_access_token = os.getenv('MAPBOX_ACCESS_TOKEN')


# Create your models here.


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=250)


class Address(models.Model):
    address = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        print(g)
        if g:
            g = g.latlng
            self.lat = g[0]
            self.long = g[1]
            print(f"Latitude: {self.lat}, Longitude: {self.long}")
        else:
            print("No latitude and longitude information found")
        return super(Address, self).save(*args, **kwargs)


class Hive(models.Model):
    title = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.title} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'hive_id': self.id})

    def save(self, *args, **kwargs):
        self.address, created = Address.objects.get_or_create(address=self.location)
        return super(Hive, self).save(*args, **kwargs)


class Comment(models.Model):
    date = models.DateField('comment date')
    content = models.TextField(max_length=250)

    hive = models.ForeignKey(
        Hive,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.date}"

class Photo(models.Model):
    url = models.CharField(max_length=200)
    hive = models.ForeignKey(Hive, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for hive_id: {self.hive_id} @{self.url}"



