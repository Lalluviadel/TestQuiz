import logging
from logging import Logger

from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.utils import timezone


from quizapp.models import BaseModel

logger: Logger = logging.getLogger(__name__)

class Card(BaseModel):
    """The model for the card."""

    ACTIVATED = 'AC'
    DEACTIVATED = 'DE'
    EXPIRED = 'EX'

    #: options for the card status
    STATUS_CHOICES = (
        (ACTIVATED, 'активирована'),
        (DEACTIVATED, 'деактивирована'),
        (EXPIRED, 'просрочена'),
    )

    card_series = models.CharField(max_length=20, blank=True, verbose_name='серия карты')
    card_number = models.CharField(max_length=20, verbose_name='номер карты')
    release_date = models.DateTimeField(default=timezone.now, verbose_name="дата выпуска карты")
    expiration_date = models.DateTimeField(default=timezone.datetime(year=2050,
                                                                     month=1,
                                                                     day=1
                                                                     ), verbose_name="дата окончания действия")
    card_status = models.CharField(choices=STATUS_CHOICES, verbose_name='статус карты', max_length=2,
                                   default=DEACTIVATED, db_index=True)

    class Meta:
        """Ordering cards according to their id."""
        ordering = ('expiration_date', 'id')
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def save(self, *args, **kwargs):
        """Automatic filling in update_time and the slug field when saving.
        """
        super().save(*args, slugified_field=self.title, **kwargs)

    def get_absolute_url(self, urlpattern_name='card_read'):
        """Returns formed url for the object."""
        return super().get_absolute_url(urlpattern_name=urlpattern_name)
