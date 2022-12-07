"""TestQuiz URL Configuration
"""
from django.contrib import admin
from django.urls import path

from quizapp.views import MainPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='index'),
    # path('users/', include('users.urls', namespace='users')),
]
