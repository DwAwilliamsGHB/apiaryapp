from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Hive
from .forms import CommentForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

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
