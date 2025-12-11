# media_tracker/admin.py

from django.contrib import admin
from .models import MediaItem # Import your model

# Register your models here.
admin.site.register(MediaItem)