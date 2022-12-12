"""Sets associations of questions application urls with their views.

Attributes:

    * app_name (str): the name of a specific web application used in different parts of the overall structure.
    * urlpatterns(list): a list of paths that determine the behavior of a web application
                         when using the urls specified in the list.
"""

from django.urls import path

from quizapp.views import TestProcessView, AnswerQuestion

app_name = 'questions'
urlpatterns = [
    path('test_body/<slug:slug>/', TestProcessView.as_view(), name='test_body'),
    path('answers/<int:question_id>/', AnswerQuestion.as_view(), name='answers'),
]
