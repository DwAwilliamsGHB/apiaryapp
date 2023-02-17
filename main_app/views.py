import os
import uuid
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Hive, Comment, Address, Photo, Like, Dislike
from .forms import CommentForm
from django.http import JsonResponse
from django.http import HttpResponseBadRequest



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

def get_hive(request, address_id):
    address = Address.objects.get(id=address_id)
    hive = address.get_hive()
    if hive:
        return JsonResponse({'hive_id': hive.id})
    else:
        return JsonResponse({'error': 'No Hive found'})

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
  return render(request, 'hives/detail.html', { 
    'hive': hive, 'comment_form': comment_form
  })

@login_required
def add_comment(request, hive_id):
  hive = get_object_or_404(Hive, id=hive_id)
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.user = request.user
      comment.hive = hive
      comment.save()
    return redirect('detail', hive_id=hive_id) 

class CommentUpdate(UpdateView):
  model = Comment
  fields = ['content']
  success_url = "/hives"

class CommentDelete(DeleteView):
  model = Comment
  success_url = "/hives"
  template_name = "main_app/comment_confirm_delete.html"

class HiveCreate(CreateView):
  model = Hive
  fields = ['title', 'location', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)

class HiveUpdate(UpdateView):
  model = Hive
  fields = ['title', 'location', 'description']

class HiveDelete(DeleteView):
  model = Hive
  success_url = '/hives'
      
def like_hive(request, hive_id):
  hive = get_object_or_404(Hive, id=hive_id)
  Like.objects.get_or_create(hive=hive, user=request.user)
  return redirect('detail', hive_id=hive_id)

def dislike_hive(request, hive_id):
  hive = get_object_or_404(Hive, id=hive_id)
  Dislike.objects.get_or_create(hive=hive, user=request.user)
  return redirect('detail', hive_id=hive_id)

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
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, hive_id=hive_id)
    except Exception as e:
      print('An error occured uploading file to S3')
      print(e)
  return redirect('detail', hive_id=hive_id)
