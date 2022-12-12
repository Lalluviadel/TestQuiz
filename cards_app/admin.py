"""Provides package integration into the admin panel."""

from django.contrib import admin
from .models import Card

class CardAdmin(admin.ModelAdmin):
    """A class for working with the Card model in the admin panel."""
    list_display = ('title', 'is_active',)
    search_fields = ('title',)
    list_filter = ('is_active',)
    fields = (('title', 'is_active'), 'card_series', 'card_number', 'release_date',
              'expiration_date', 'card_status')


admin.site.register(Card, CardAdmin)


