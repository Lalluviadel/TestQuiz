import datetime
import logging
import random
import time
from logging import Logger

from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, DeleteView

from cards_app.models import Card
from quizapp.mixins import TitleMixin, AuthorizedOnlyDispatchMixin

logger: Logger = logging.getLogger(__name__)


class CardListView(ListView, TitleMixin):
    """View for the card list.
    Сhecking whether the status of expired cards needs to be changed."""
    model = Card
    template_name = 'cards/cards_list.html'
    title = 'Список карт'
    paginate_by = 5

    def get_queryset(self):
        """Start checking whether the status of expired cards needs to be changed.
        Returns a queryset of all active cards.
        """
        self.processing_exp_date_cards()
        return Card.objects.filter(is_active=True)

    @staticmethod
    def processing_exp_date_cards():
        """Сhecking whether the status of expired cards needs to be changed."""
        exp_date_cards_ids = list(Card.objects.filter(expiration_date__lte=timezone.now()).
                                  exclude(card_status='EX').
                                  values_list('id', flat=True))
        if exp_date_cards_ids:
            for card_id in exp_date_cards_ids:
                card = Card.objects.get(id=card_id)
                card.card_status = 'EX'
                card.save()


class CardSearchView(ListView, TitleMixin):
    """View to display the search results for cards (when using the site search bar).
    The search is performed by card_series, card_number, release_date,
    expiration_date, card_status.
    """
    model = Card
    template_name = 'cards/search_options_page.html'
    title = 'Поиск по картам'

    def post(self, request, *args, **kwargs):
        """Returns a queryset filtered for the presence of a match with the data entered by the user."""
        try:
            search_options = ['card_series', 'card_number', 'start_date', 'expired_date', 'status']
            searсh_conditions = [request.POST.get(i) for i in search_options if i in request.POST]
            release_start_date, release_end_date = self.search_date_conditions_processing(searсh_conditions[2])
            expiration_start_date, expiration_end_date = self.search_date_conditions_processing(searсh_conditions[3])

            query = Card.objects.filter(Q(card_series__icontains=searсh_conditions[0])
                                        & Q(card_number__icontains=searсh_conditions[1])
                                        & Q(release_date__gte=release_start_date,
                                            release_date__lte=release_end_date
                                            )
                                        & Q(expiration_date__gte=expiration_start_date,
                                            expiration_date__lte=expiration_end_date
                                            ))
            if searсh_conditions[4]:
                query = query.filter(card_status=searсh_conditions[4])

            context = {
                'card_list': query,
                'title': self.title,
            }

            return render(request, 'cards/cards_list.html', context=context)
        except Exception as err:
            template = "An exception of type {0} occurred during processing cards search conditions. Arguments:\n{1!r}"
            message = template.format(type(err).__name__, err.args)
            logger.info(message)
            context = {
                'error_checking': 'Извините, при поиске произошла ошибка. Пожалуйста, попробуйте еще раз',
                'title': self.title,
            }

            return render(request, 'cards/cards_list.html', context=context)

    def search_date_conditions_processing(self, datetime_str: str):
        """
        Processes and returns datetime objects of the search start and end dates (search time range).
        If the date is not set by the user, returns datetime objects: 1900.01.01 and 2050.01.01.
        """
        if datetime_str:
            start_date = self.datetime_processing(datetime_str)
            end_date = start_date + datetime.timedelta(days=1)
        else:
            start_date = self.datetime_processing('1900-01-01')
            end_date = self.datetime_processing('2050-01-01')
        return start_date, end_date

    @staticmethod
    def datetime_processing(datetime_str: str):
        """Gets a string, returns a datetime object."""
        return datetime.datetime.strptime(datetime_str, '%Y-%m-%d')


class CardDetail(TitleMixin, DetailView, AuthorizedOnlyDispatchMixin):
    """View to viewing a card profile with its purchase history."""
    title = 'Профиль карты'
    model = Card
    template_name = 'cards/card_detail.html'
    slug_url_kwarg = 'card_slug'


class CardDeleteView(DeleteView, AuthorizedOnlyDispatchMixin):
    """View to card delete and activate/deactivate."""
    slug_url_kwarg = 'card_slug'
    model = Card
    template_name = 'cards/card_detail.html'
    success_url = reverse_lazy('cards:cards_list')

    def delete(self, request, *args, **kwargs):
        """Performs complete deletion or activation/deactivation of the object
        in accordance with the specified mode of action.
        """
        item = self.get_object()
        if 'no_delete' in request.POST:
            if item.card_status != 'EX':
                item.card_status = 'AC' if item.card_status == 'DE' else 'DE'
                item.save()
        else:
            item.is_active = not item.is_active
            item.save()

    def post(self, request, *args, **kwargs):
        """Starts the process of deleting or activating/deactivating category.
        When enabled ajax, returns data for an asynchronous web request.
        """
        self.delete(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('cards:cards_list'))


class CardGeneratorView(TitleMixin, ListView):
    """View to card generating in accordance with the specified requirements."""
    title = 'Сгенерировать карты'
    template_name = 'cards/card_generator.html'
    model = Card

    def post(self, request, *args, **kwargs):
        """
        Gets the conditions for generating new cards. Processes the received data.
        Create cards according to the conditions.
        Switching to the page with the list of generated cards.
        """
        try:
            new_cards_queryset = Card.objects.none()

            card_series = request.POST.get('card_series')
            quantity = int(request.POST.get('quantity'))
            exp_date = request.POST.get('exp_date')

            now = timezone.now()
            exp_date_map = {
                'year': now + relativedelta(years=1),
                'half_year': now + relativedelta(months=6),
                'month': now + relativedelta(months=1),
            }

            for number in range(quantity):
                card_number = str(time.time()).split('.')[1]
                instance = Card.objects.create(title=f'Card_{number + 1}_{card_number}', card_series=card_series,
                                               card_number=card_number, expiration_date=exp_date_map[exp_date],
                                               card_status=random.choice(['DE', 'AC']))
                new_cards_queryset |= Card.objects.filter(id=instance.id)

        except Exception as err:
            template = "An exception of type {0} occurred processing cards generator conditions. Arguments:\n{1!r}"
            message = template.format(type(err).__name__, err.args)
            logger.info(message)
            context = {
                'error_checking': 'Извините, при генерации карт произошла ошибка. Пожалуйста, попробуйте еще раз',
                'title': self.title,
            }

            return render(request, 'cards/cards_list.html', context=context)

        context = {
            'title': 'Сгенерированные вами карты',
            'card_list': new_cards_queryset,
        }

        return render(request, 'cards/cards_list.html', context=context)
