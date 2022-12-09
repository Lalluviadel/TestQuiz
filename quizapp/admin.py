from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.forms import ModelForm, Textarea
from django.utils.html import format_html

from quizapp.models import Category, Question, QuestionSet

admin.site.site_header = 'Админ-панель тестового задания для ИП Авдеев В.Ю. "'
admin.site.site_title = 'Тестовое задание для ИП Авдеев В.Ю. "'


class BigTextBodyForm(ModelForm):
    """A form for the question set admin panel that uses a more convenient widget for large text."""

    class Meta:
        """Defining a widget for a field."""
        model = Question
        widgets = {
            'text': Textarea
        }
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    """A class for working with the Category model in the admin panel."""
    list_display = ('title', 'is_active', 'view_questions_link',)
    search_fields = ('title',)
    list_filter = ('is_active',)
    fields = (('title', 'is_active'), 'description',)

    def delete_queryset(self, request, queryset):
        """Defines the behavior when deleting a set.
        The object will not be deleted, but deactivated."""
        for item in queryset:
            item.delete()

    def view_questions_link(self, obj: Category):
        """Сreating a table list field with number of questions in this category."""
        count = obj.question_set.count()
        return format_html('<span>Кол-во вопросов: {}</span>', count)

    view_questions_link.short_description = "Вопросов в категории"


class QuestionInline(GenericStackedInline):
    """A class for working with the Question model in the admin panel (inline,
    as part of editing QuestionSet)."""
    model = Question
    form = BigTextBodyForm
    fields = ('text', ('category', 'is_active'),
              ('answer_01', 'answer_02', 'answer_03', 'answer_04',),
              'right_answers',)
    extra = 1


class QuestionSetAdmin(admin.ModelAdmin):
    """A class for working with the QuestionSet model in the admin panel."""
    list_display = ('title', 'is_active')
    search_fields = ('title',)
    list_filter = ('is_active',)
    fields = (('title', 'is_active'), 'description', )
    inlines = [QuestionInline, ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
