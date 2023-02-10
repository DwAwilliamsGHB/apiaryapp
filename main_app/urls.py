from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('hives/', views.hives_index, name='index'),
    path('hives/create/', views.HiveCreate.as_view(), name='hives_create'),
    path('hives/<int:hive_id>/', views.hives_detail, name='detail'),
    path('hives/<int:pk>/update/', views.HiveUpdate.as_view(), name='hives_update'),
    path('hives/<int:pk>/delete/', views.HiveDelete.as_view(), name='hives_delete'),
    path('hives/<int:hive_id>/add_comment/', views.add_comment, name='add_comment'),
    path('accounts/signup/', views.signup, name='signup'),

]