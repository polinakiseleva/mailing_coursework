from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView as MyLoginView, LogoutView as MyLogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserForm
from users.models import User


class LoginView(MyLoginView):
    template_name = 'users/login.html'


class LogoutView(MyLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация на сайте', }

    def form_valid(self, form):
        self.object = form.save()

        if form.is_valid():
            send_mail(
                subject='Поздравляем с регистрацией',
                message='Вы зарегистрировались на нашей платформе, добро пожаловать!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email],
                fail_silently=False,
            )
            group = Group.objects.get(name='ordinary')
            self.object.groups.add(group)
        return super().form_valid(form)
