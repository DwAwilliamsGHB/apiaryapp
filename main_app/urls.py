from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('hives/', views.hives_index, name='index'),
    path('profile/', views.profile_detail, name='profile'),
    path('hives/create/', views.HiveCreate.as_view(), name='hives_create'),
    path('hives/<int:hive_id>/', views.hives_detail, name='detail'),
    path('hives/<int:pk>/update/', views.HiveUpdate.as_view(), name='hives_update'),
    path('hives/<int:pk>/delete/', views.HiveDelete.as_view(), name='hives_delete'),
    path('hives/<int:hive_id>/add_comment/', views.add_comment, name='add_comment'),
    path('<pk>/update/', views.CommentUpdate.as_view(), name='update_comment'),
    path('<pk>/delete/', views.CommentDelete.as_view(), name='delete_comment'),
    path('hives/<int:hive_id>/like/', views.like_hive, name='like_hive'),
    path('hives/<int:hive_id>/dislike/', views.dislike_hive, name='dislike_hive'),
    path('hives/<int:hive_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
    path('hives/<int:hive_id>/location/', views.location_detail, name='location_details'),
    path('addresses/<int:address_id>/hive/', views.get_hive, name='get_hive'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    