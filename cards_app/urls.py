"""Sets associations of cards_app application urls with their views.

Attributes:

    * app_name (str): the name of a specific web application used in different parts of the overall structure.
    * urlpatterns(list): a list of paths that determine the behavior of a web application
                         when using the urls specified in the list.
"""

from django.urls import path

from cards_app.views import CardListView, CardSearchView, CardDetail, CardDeleteView, CardGeneratorView

app_name = 'cards'
urlpatterns = [
    path('', CardListView.as_view(), name='cards_list'),
    path('search-options', CardSearchView.as_view(), name='search-options'),
    path('detail/<slug:card_slug>/', CardDetail.as_view(), name='card_read'),
    path('cards-delete/<slug:card_slug>/', CardDeleteView.as_view(), name='card_delete'),
    path('cards-generator', CardGeneratorView.as_view(), name='cards_generator'),
]
