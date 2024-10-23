from django.contrib import admin
from .models import Item, Storage, Bin, Stored_Item

admin.site.register(Item)
admin.site.register(Storage)
admin.site.register(Bin)
admin.site.register(Stored_Item)