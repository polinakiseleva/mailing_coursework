from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = user.pk
    verification_link = reverse_lazy('users:verify_email', kwargs={'uidb64': uid, 'token': token})
    site = settings.SITE_ADRES
    subject = 'Поздравляем Вас с регистрацией!'
    message = f'Для активации аккаунта перейдите по ссылке: {site}{verification_link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

    # устанавливаем флаг, что сообщение было отправлено
    user.email_verified = True
    user.save()
