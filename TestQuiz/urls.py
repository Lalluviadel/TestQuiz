"""TestQuiz URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from quizapp.views import MainPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='index'),
    path('questions/', include('quizapp.urls', namespace='quizapp')),
    path('users/', include('users.urls', namespace='users')),
]
