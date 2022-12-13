import datetime
import logging
from logging import Logger

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from cards_app.models import Card
from quizapp.mixins import TitleMixin

logger: Logger = logging.getLogger(__name__)


class CardListView(ListView, TitleMixin):
    """View for the card list."""
    model = Card
    template_name = 'cards/cards_list.html'
    title = 'Список карт'

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
            logger.info('Exception during processing cards search condition: %s', err)
            context = {
                'error_checking': 'Извините, при поиске произошла ошибка. Пожалуйста, попробуйте еще раз',
                'title': self.title,
            }

            return render(request, 'cards/cards_list.html', context=context)
    def search_date_conditions_processing(self, datetime_str: str):
        """
        Processes and returns datetime objects of the search start and end dates (search time range).
        If the date is not set by the user, returns datetime objects: 1900.01.01 and 1900.01.01.
        """
        if datetime_str:
            start_date = self.datetime_processing(datetime_str)
            end_date = start_date + datetime.timedelta(days=1)
        else:
            start_date = self.datetime_processing('1900-01-01')
            end_date = self.datetime_processing('1900-01-01')
        return start_date, end_date

    @staticmethod
    def datetime_processing(datetime_str: str):
        """Gets a string, returns a datetime object."""
        return datetime.datetime.strptime(datetime_str, '%Y-%m-%d')


class CardDetail(TitleMixin, DetailView):
    """View to viewing a card profile with its purchase history."""
    title = 'Профиль карты'
    model = Card
    template_name = 'cards/card_detail.html'
    slug_url_kwarg = 'card_slug'
