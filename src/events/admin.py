from django.contrib import admin

from events.models import Event,Categorie


# Register your models here.
@admin.register(Event)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'type','image_tag','status']
    list_filter = ('type','category')

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview','image_tag']
