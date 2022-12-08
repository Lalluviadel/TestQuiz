import logging
from logging import Logger

from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.db import models, transaction
from django.urls import reverse
from django.utils import timezone
from pytils.translit import slugify
from django.core.exceptions import ValidationError

logger: Logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    """Base class for Category and QuestionSet models."""
    title = models.CharField(max_length=250, unique=True, verbose_name='наименование')
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
        """The object will not be deleted, but deactivated."""
        self.is_active = not self.is_active
        self.save()


class Category(BaseModel):
    """The model for the category."""
    description = models.TextField(blank=True, verbose_name="описание")

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


class Question(models.Model):
    """The model for the question."""

    text = models.CharField(max_length=250, default='question', verbose_name="текст вопроса")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='1', verbose_name="категория")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="время создания")
    update_time = models.DateTimeField(default=timezone.now, verbose_name="время изменения")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="активен")

    right_answers = models.CharField(max_length=50, default='1,', verbose_name="правильный ответ/ответы")
    answer_01 = models.CharField(max_length=150, blank=True, verbose_name="ответ №1")
    answer_02 = models.CharField(max_length=150, blank=True, verbose_name="ответ №2")
    answer_03 = models.CharField(max_length=150, blank=True, verbose_name="ответ №3")
    answer_04 = models.CharField(max_length=150, blank=True, verbose_name="ответ №4")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        """Ordering questions according to their id."""
        ordering = ('id',)
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        """Forms and returns a printable representation of the object."""
        return str(self.text)

    def clean(self):
        """Checking the values passed in the model field."""
        self.right_answers_processing()

    def right_answers_processing(self):
        """Validating the values of the right answers field.
        - only numbers in the range from 1 to the number of possible answers should be specified;
        - all the answers cannot be right;
        """
        msg = "В правильных ответах к вопросу указывайте только цифры!"
        try:
            right_answers_no_whitespace = self.right_answers.replace(" ", "")
            right_answers_only_int = [int(r_ans) for r_ans in right_answers_no_whitespace.split(',') if r_ans]

            number_non_empty_answers = len([answer for answer in
                                            [self.answer_01, self.answer_02, self.answer_03, self.answer_04]
                                            if answer])

            # we check that the number of each right answer is in the range
            # between 0 and the number of possible answers
            right_answers_check = all(map(lambda x: 1 <= x <= number_non_empty_answers, right_answers_only_int))
            if not right_answers_check or not right_answers_only_int \
                    or len(right_answers_only_int) >= number_non_empty_answers:
                msg = "Проверьте количество и значение указанных правильных ответов!"
                raise ValueError

        except ValueError as err:
            logger.info('An error was processed during right_answers checking')
            raise ValidationError(
                {'right_answers': msg}) from err


class QuestionSet(BaseModel):
    """The model for the question set."""
    questions = GenericRelation('Question')

    class Meta:
        """Ordering questions according to their id."""
        ordering = ('id',)
        verbose_name = 'Набор тестов'
        verbose_name_plural = 'Наборы тестов'

    def save(self, *args, **kwargs):
        """Automatic filling in update_time and the slug field when saving.
        """
        super().save(*args, slugified_field=self.title, **kwargs)

    def get_absolute_url(self, urlpattern_name='questionset_read'):
        """Returns formed url for the object."""
        return super().get_absolute_url(urlpattern_name=urlpattern_name)
