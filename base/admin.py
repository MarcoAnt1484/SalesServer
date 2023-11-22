from django.contrib import admin

# Register your models here.

from .models import Sales, Inventory

admin.site.register(Sales)
admin.site.register(Inventory)