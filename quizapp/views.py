from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import ContextMixin

from quizapp.models import Category


class TitleMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class MainPageView(ListView, TitleMixin):
    """View for the categories of tests page."""
    model = Category
    template_name = 'index.html'
    title = 'Категории тестов'

