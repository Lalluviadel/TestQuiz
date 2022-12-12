"""Sets associations of cards_app application urls with their views.

Attributes:

    * app_name (str): the name of a specific web application used in different parts of the overall structure.
    * urlpatterns(list): a list of paths that determine the behavior of a web application
                         when using the urls specified in the list.
"""

from django.urls import path

from cards_app.views import CardListView

app_name = 'cards'
urlpatterns = [
    path('', CardListView.as_view(), name='cards_list'),
]
