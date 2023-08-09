from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from users.utils import send_verification_email


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()
        new_user = form.save()
        send_verification_email(new_user)
        return redirect('users:verify_email_sent')


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = uidb64
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user


class VerifyEmailSentView(View):
    def get(self, request):
        return render(request, 'users/verify_email_sent.html')


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'
