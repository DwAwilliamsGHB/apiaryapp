from django.contrib import admin
from .models import Hive, Comment, Address

# Register your models here.
admin.site.register(Hive)
admin.site.register(Comment)
admin.site.register(Address)

