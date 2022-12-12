"""
The submodule contains views for a full-fledged user interaction with the content of the site.

Here are the views:

    * to register a new user and verify a registration of a profile;
    * to log in and log out of the profile;
    * to recover forgotten password;

"""
import logging
from smtplib import SMTPAuthenticationError

from django.contrib import auth, messages
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, LoginView, LogoutView, \
    PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from TestQuiz.settings import DOMAIN_NAME, EMAIL_HOST_USER
from quizapp.views import TitleMixin
from users.forms import UserLoginForm, UserRegisterForm, UserPasswordResetForm
from users.models import QuizUser

logger = logging.getLogger(__name__)


class UserLoginView(LoginView, TitleMixin):
    """A view for authorization."""
    template_name = 'registration/login.html'
    title = 'Авторизация'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        """Performs user authorization. Authorization is performed only for active users
        (who have verified their profile with a link received by email)."""
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'registration/login.html', context={'form': form, })


class RegisterView(FormView, TitleMixin):
    """A view for registering a new user."""
    template_name = 'registration/register.html'
    title = 'Регистрация нового пользователя'
    form_class = UserRegisterForm

    def post(self, request, *args, **kwargs):
        """Performs registration of a new user.
        Both in case of success and in case of failure, a message is generated
        that shows the user the result of registration.
        Starts the verification process of the new profile."""
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            try:
                if self.send_verify_link(user):
                    messages.success(request, 'Для завершения регистрации используйте ссылку из письма, отправленного '
                                              'на email, указанный при регистрации.')

                else:
                    msg = f'К сожалению, произошел сбой, письмо для завершения регистрации не было отослано. ' \
                          f'Для активации вашего профиля напишите письмо на адрес {EMAIL_HOST_USER}'
                    messages.error(request, msg)
                return HttpResponseRedirect(reverse('users:register'))
            except SMTPAuthenticationError:
                messages.error(request, 'К сожалению, произошел сбой. Пользователь с указанными данными не был'
                                        'зарегистрирован.')
                logger.error('SMTPAuthenticationError while user registration')
                user.delete()
                return render(request, 'registration/register.html', context={'form': form, })
        else:
            messages.error(request, 'Убедитесь, что вы ввели корректные данные.')
            logger.warning('Неудачная попытка регистрации пользователя')
        return render(request, 'registration/register.html', context={'form': form, })

    @staticmethod
    def send_verify_link(user):
        """Send to user an email with verification link.

        Args:

            * user(QuizUser): the user object that was created during registration;

        """
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        subject = f"Подтверждение регистрации на сайте {DOMAIN_NAME}"
        context = {
            'my_user': user.username,
            'my_site_name': DOMAIN_NAME,
            'my_link': f'{DOMAIN_NAME}{verify_link}',
        }
        message = render_to_string('registration/activation_msg.html', context)
        return send_mail(subject, message, EMAIL_HOST_USER, [user.email],
                         html_message=message, fail_silently=False)


class Verify(TemplateView, TitleMixin):
    """A view for activating and authorizing a new user."""
    title = 'Успешная активация профиля'

    def get(self, request, *args, **kwargs):
        """Checks the validity period of the activation key and its
        compliance with the one that is in the activation link sent
        to the user. If successful, the user becomes active and logs in.
        In case of failure, an appropriate message is generated to inform the user
        about this and further options for action."""
        try:
            user = QuizUser.objects.get(email=kwargs['email'])

            if user.is_activation_key_expired():
                msg = f'Ваш ключ активации устарел. ' \
                      f'Для активации вашего профиля напишите письмо на адрес {EMAIL_HOST_USER} ' \
                      f'или зарегистрируйте новый профиль, используя другой email.'
                logger.error(f'Сбой активации нового пользователя - устаревший ключ активации')
                return HttpResponseRedirect(reverse('users:failed', kwargs={'error': msg}))

            elif user and user.activation_key == kwargs['activation_key']:
                user.activation_key, user.activation_key_created = '', None
                user.is_active = True
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                user.save()
                return render(request, 'registration/verification.html')

            else:
                raise ValueError('Несовпадение ключа активации из письма с присвоенным пользователю')

        except Exception as e:
            logger.error(f'Сбой активации нового пользователя - {e}')
            msg = f'Сбой активации. Попробуйте использовать ссылку, полученную в письме, повторною. ' \
                  f'В случае неудачи напишите на адрес {EMAIL_HOST_USER}, указав причину обращения.'
            return HttpResponseRedirect(reverse('users:failed', kwargs={'error': msg}))


class FailedAuthenticationView(TemplateView):
    """View for failed authorization completion.
    If activation user's profile or VK-authentication is failed,
    the user will be redirected with an error message."""

    def get(self, request, *args, **kwargs):
        """Receives an error message that was made during authorization and passes it to the context."""
        return render(request, 'registration/attempt_failed.html', context={
            'error': kwargs['error'], 'title': 'Неудачная авторизация',
        })


class UserLogoutView(LogoutView):
    """A view for the user to log out of the profile."""
    next_page = 'index'


class UserPasswordResetView(PasswordResetView, TitleMixin):
    """A view to request password recovery."""
    form_class = UserPasswordResetForm
    title = 'Восстановление пароля'
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/pass_reset_email.html'
    subject_template_name = 'registration/pass_reset_subject.txt'
    from_email = EMAIL_HOST_USER

    def post(self, request, *args, **kwargs):
        """Generates and sends the user an email with a link to restore the password."""
        form = self.form_class(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            context = {
                'email': email,
                'domain': DOMAIN_NAME,
            }
            form.save(DOMAIN_NAME, email_template_name=self.email_template_name,
                      subject_template_name=self.subject_template_name, from_email=self.from_email,
                      extra_email_context=context)
            return render(request, 'registration/password_reset_email_sent.html', {'title': self.title})
        return render(request, 'registration/password_reset.html', context={'form': form, 'title': self.title})


class MyPasswordResetConfirmView(PasswordResetConfirmView, TitleMixin):
    """A view for creating and saving a new password in case the previous password was lost by the user."""
    template_name = 'registration/password_res_confirm.html'
    title = 'Создание нового пароля'


class MyPasswordResetCompleteView(PasswordResetCompleteView, TitleMixin):
    """A view to inform the user about the successful change (recovery) of the password."""
    template_name = 'registration/password_res_complete.html'
    title = 'Пароль успешно изменен'
