

from events.models import Event,Categorie,Guest

from django.contrib import admin
import csv
import io

from django.http import HttpResponse
from django.contrib import admin



from reportlab.pdfgen import canvas

import csv

from django.http import HttpResponse
from django.utils.encoding import  smart_str

def export_guests_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guests.csv"'

    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))

    writer.writerow([
        smart_str(u"Nom de l'événement"),
        smart_str(u"Nom de l'invité"),
        smart_str(u"Statut de l'invité"),
        smart_str(u"Feedback de l'invité"),
        smart_str(u"Notation de l'invité"),
        smart_str(u"Date de création")
    ])

    for obj in queryset:
        for guest in obj.guest_set.all():
            writer.writerow([
                smart_str(obj.title),
                smart_str(guest.user.nom),
                smart_str(guest.status),
                smart_str(guest.feedback),
                smart_str(guest.rating),
                smart_str(guest.created_at),
            ])

    return response

export_guests_csv.short_description = "Exporter les invités sélectionnés au format CSV"

def export_guests_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="guests.pdf"'

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)
    p.setFont('Helvetica-Bold', 16)
    p.drawString(100, 750, 'Liste des invités par événement')

    y = 700
    for event in queryset:
        guests = Guest.objects.filter(event=event)
        p.setFont('Helvetica', 14)
        p.drawString(100, y, event.title)
        y -= 20
        p.setFont('Helvetica', 12)
        for guest in guests:
            p.drawString(120, y, guest.user.nom)
            p.drawString(220, y, guest.user.prenom)
            p.drawString(350, y, guest.feedback)

            y -= 15
        y -= 20

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

export_guests_pdf.short_description = 'Exporter les invités sélectionnés en PDF'

class GuestInline(admin.TabularInline):
    model = Guest
    fk_name = 'event'
    extra = 0

# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [GuestInline]
    list_display = ['title', 'price', 'type','image_tag','status']
    list_filter = ('type','category')
    actions = [export_guests_pdf,export_guests_csv]

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview','image_tag']
