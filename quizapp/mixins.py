from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.base import ContextMixin, View


class TitleMixin(ContextMixin):
    """Adds the page title to the view"""
    title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

class AuthorizedOnlyDispatchMixin(View):
    """Access to the view only for authorized users."""
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
