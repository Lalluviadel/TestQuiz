from django.contrib import admin

from quizapp.models import Category

admin.site.site_header = 'Админ-панель тестового задания для ИП Авдеев В.Ю. "'


class CategoryAdmin(admin.ModelAdmin):
    """A class for working with the Category model in the admin panel."""
    list_display = ('title', 'is_active')
    search_fields = ('title',)
    list_filter = ('is_active',)
    fields = (('title', 'is_active'), 'description', )

admin.site.register(Category, CategoryAdmin)
