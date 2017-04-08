from django.contrib import admin

# Register your models here.
from .models import Category, Forum, Contents, Torrents, Vers

admin.site.register(Category)
admin.site.register(Forum)
admin.site.register(Torrents)
admin.site.register(Contents)
admin.site.register(Vers)