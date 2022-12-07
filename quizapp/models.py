import logging
from logging import Logger

from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from pytils.translit import slugify
from django.db import models, transaction

logger: Logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    """Base class for Category and ... models."""
    title = models.CharField(max_length=150, unique=True, verbose_name='наименование')
    create_time = models.DateTimeField(default=timezone.now, verbose_name="время создания")
    update_time = models.DateTimeField(default=timezone.now, verbose_name="время изменения")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="активен")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        """Specifying an abstract class."""
        abstract = True

    def __str__(self):
        """Forms and returns a printable representation of the object.
        """
        return str(self.title)

    def save(self, *args, slugified_field=None, **kwargs):
        """Automatic filling in 'update_time' and 'slug' fields when saving."""
        self.update_time = timezone.now()
        if slugified_field:
            try:
                with transaction.atomic():
                    self.slug = old_slug = slugify(slugified_field)
                    super().save(*args, **kwargs)
            except IntegrityError:
                with transaction.atomic():
                    self.slug = slugify(slugified_field + str(timezone.now()))
                    logger.info('Non-unique slug %s replaced with %s', old_slug, self.slug)
                    super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def get_absolute_url(self, urlpattern_name: str):
        """Returns formed url for the object."""
        return reverse(urlpattern_name, args=[str(self.slug)])

    def delete(self, using=None, keep_parents=False):
        self.is_active = False if self.is_active is False else True
        self.save()


class Category(BaseModel):
    """The model for the category."""
    description = models.TextField(blank=True)

    class Meta:
        """Ordering categories according to their id."""
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        """Automatic filling in update_time and the slug field when saving.
        """
        super().save(*args, slugified_field=self.title, **kwargs)


    def get_absolute_url(self, urlpattern_name='category_read'):
        """Returns formed url for the object."""
        return super().get_absolute_url(urlpattern_name=urlpattern_name)

