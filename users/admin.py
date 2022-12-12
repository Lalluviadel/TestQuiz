"""Provides package integration into the admin panel."""

from django.contrib import admin
from .models import QuizUser

class QuizUserAdmin(admin.ModelAdmin):
    """A class for working with the QuizUser model in the admin panel."""
    list_display = ('last_name', 'first_name', 'username', 'is_active')
    search_fields = ('last_name', 'first_name', 'username',)
    list_filter = ('is_active', 'date_joined',)
    fields = (('last_name', 'first_name',), 'username', ('is_superuser', 'is_staff',),
              ('email', 'date_joined',))
    readonly_fields = ('email', 'date_joined',)


admin.site.register(QuizUser, QuizUserAdmin)
