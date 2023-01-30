from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Items)
admin.site.register(ItemProperty)
admin.site.register(Properties)
admin.site.register(PriceDynamic)


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'item_url')
    list_filter = ('title', 'price')
