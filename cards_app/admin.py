"""Provides package integration into the admin panel."""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Card, Order


class CardAdmin(admin.ModelAdmin):
    """A class for working with the Card model in the admin panel."""
    list_display = ('title', 'is_active', 'view_orders_link',)
    search_fields = ('title',)
    list_filter = ('is_active',)
    fields = (('title', 'is_active'), 'card_series', 'card_number', 'release_date',
              'expiration_date', 'card_status')

    def view_orders_link(self, obj: Card):
        """Сreating a table list field with number of questions in this category."""
        count = obj.order_set.count()
        url = (reverse("admin:cards_app_order_changelist")
               + "?" + urlencode({"card_used__title": f"{obj.title}"}))
        return format_html('<a href="{}">Кол-во покупок: {}</a>', url, count)

    view_orders_link.short_description = "Покупок с этой картой"

class OrderAdmin(admin.ModelAdmin):
    """A class for working with the Order model in the admin panel."""
    list_display = ('use_time', 'order_amount', 'card_used', 'is_active',)
    search_fields = ('use_time',)
    list_filter = ('is_active', 'use_time',)
    fields = (('card_used', 'is_active'), 'use_time', 'order_amount',)


admin.site.register(Card, CardAdmin)
admin.site.register(Order, OrderAdmin)
