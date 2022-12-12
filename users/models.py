"""
Stores the user model that is necessary for the interaction of site visitors with its content.
"""
from datetime import timedelta
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class QuizUser(AbstractUser):
    """The model for the user."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False, db_index=True)
    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        """Forms a printable representation of the object.
        Returns user's firstname and username.
        """
        return f'{self.first_name} "{self.username}"'

    def is_activation_key_expired(self):
        """If the user has not managed to activate his profile during this time,
        he will have to register again.
        """
        if now() <= self.activation_key_created + timedelta(hours=48):
            return False
        return True
