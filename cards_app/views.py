from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from cards_app.models import Card
from quizapp.mixins import TitleMixin


class CardListView(ListView, TitleMixin):
    """View for the card list."""
    model = Card
    template_name = 'cards/cards_list.html'
    title = 'Список карт'

