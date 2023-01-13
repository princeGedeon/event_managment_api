from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import User


class UserModelAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email', 'nom','prenom', 'is_admin','profile','image_tag')
    list_filter = ('is_admin','profile')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nom','prenom','number_phone',)}),
        ('Permissions', {'fields': ('is_admin','profile')}),
        ('Localisation', {'fields': ('longitude','latitude')}),

    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom','prenom', 'password1', 'password2'),
        }),
    )
    search_fields = ('email','nom','prenom')
    ordering = ('id','email',)
    filter_horizontal = ()



admin.site.register(User, UserModelAdmin)