import datetime

from django.db import models

from accounts.models import User
from django.utils.safestring import mark_safe


TYPE_EVENT = (
    ("PUBLIC", "PUBLIC"),
    ("PRIVE", "PRIVE"),
)

STATUS_EVENT = (
    ("ACTIVE", "ACTIVE"),
    ("CLOSED", "CLOSED"),
)

# Create your models here.
class Categorie(models.Model):
    preview=models.ImageField(upload_to="categorie_images",default="default2.jpg")
    title=models.CharField(max_length=200)
    description=models.TextField(default="Pas de description")

    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.preview.url))

    def __str__(self):
        return self.title

class Event(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField(default="Pas de description")
    date_created=models.DateTimeField(auto_now_add=True)
    preview=models.ImageField(upload_to="event_images",default="default.jpg")
    type=models.CharField(max_length=100,choices=TYPE_EVENT,default="PRIVE")
    code_adhesion=models.CharField(max_length=20,default="")
    price = models.DecimalField(max_digits=15,decimal_places=2,default=0.0)
    category=models.ForeignKey(Categorie,on_delete=models.CASCADE)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name="Date de debut de l'évenement",default=datetime.datetime.now())
    end_date_inscription = models.DateTimeField(verbose_name="Date cloture de l'inscription")
    status=models.CharField(max_length=100,default="ACTIVE",choices=STATUS_EVENT)
    location = models.CharField(max_length=255,default="En ligne")
    number_phone = models.CharField(max_length=20)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    is_active=models.BooleanField(default=True)



    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.preview.url))

    def __str__(self):
        return self.title