"""Contains custom commands for easy launch by manage.py."""
from users.models import QuizUser
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """A command for quickly creating a superuser."""
    def handle(self, *args, **options):
        user = QuizUser.objects.create_superuser('admin', 'admin@admin.ru', '12345')
        user.is_active = True
        user.save()

