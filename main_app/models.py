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
    
    def get_hive(self):
        try:
            return Hive.objects.get(address=self)
        except Hive.DoesNotExist:
            return None


class Hive(models.Model):
    title = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)

    def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dislikes(self):
        return self.dislikes.users.count()

    def __str__(self):
        return f'{self.title} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'hive_id': self.id})

    def save(self, *args, **kwargs):
        self.address, created = Address.objects.get_or_create(address=self.location)
        return super(Hive, self).save(*args, **kwargs)


class Comment(models.Model):
    user =  models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    hive = models.ForeignKey(
        Hive,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.content)[:30]

class Like(models.Model):

    hive = models.OneToOneField(Hive, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_hive_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment.content)[:30]
       
class DisLike(models.Model):

    hive = models.OneToOneField(Hive, related_name="dislikes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_hive_dislikes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment.content)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    hive = models.ForeignKey(Hive, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for hive_id: {self.hive_id} @{self.url}"
