import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Hive, Address, Photo
from .forms import CommentForm


# Create your views here.
def home(request):
  mapbox_access_token = os.environ.get('MAPBOX_ACCESS_TOKEN')
  default_lat = 40.7128
  default_long = -74.0060
  addresses = Address.objects.all()
  print(addresses)  # Debug statement to check the queryset
  return render(request, 'home.html', {
    'mapbox_access_token': mapbox_access_token,
    'default_lat': default_lat,
    'default_long': default_long,
    'addresses': addresses,
  })


def about(request):
  return render(request, 'about.html')

@login_required
def hives_index(request):
  hives = Hive.objects.all()
  return render(request, 'hives/index.html', {
    'hives': hives
  })

def hives_detail(request, hive_id):
  hive = Hive.objects.get(id=hive_id)
  comment_form = CommentForm()
  return render(request, 'hives/detail.html', { 'hive': hive, 'comment_form': comment_form
  })

def add_comment(request, hive_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.hive_id = hive_id
    new_comment.save()
  return redirect('detail', hive_id=hive_id) 

class HiveCreate(CreateView):
  model = Hive
  fields = ['title', 'location', 'description']

class HiveUpdate(UpdateView):
  model = Hive
  fields = ['title', 'location', 'description']

class HiveDelete(DeleteView):
  model = Hive
  success_url = '/hives'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def location_detail(request, hive_id):
    hive = Hive.objects.get(id=hive_id)
    mapbox_access_token = os.environ.get('MAPBOX_ACCESS_TOKEN')
    address = hive.address
    lat = address.lat
    long = address.long
    return render(request, 'location.html', {
        'mapbox_access_token': mapbox_access_token,
        'lat': lat,
        'long': long,
    })
  
def add_photo(request, hive_id):
  photo_file = request.FILES.get('photo_file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S#_BUCKET_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, hive_id=hive_id)
    except Exception as e:
      print('An error occured uploading file to S3')
      print(e)
  return redirect('detail', hive_id=hive_id)
