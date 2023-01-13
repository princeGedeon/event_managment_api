from django.contrib import admin

from events.models import Event,Categorie,Guest

class GuestInline(admin.TabularInline):
    model = Guest
    fk_name = 'event'

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [GuestInline]
    list_display = ['title', 'price', 'type','image_tag','status']
    list_filter = ('type','category')

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview','image_tag']
