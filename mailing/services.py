from django.core.mail import send_mail

from mailing.models import Message, Log, Mail
from django.core.cache import cache

from config import settings


def daily_send():
    for item in Mail.objects.filter(frequency='daily'):
        item.status = 'running'
        item.save()
        send_mail(item)
        item.status = 'completed'
        item.save()


def weekly_send():
    for item in Mail.objects.filter(frequency='weekly'):
        item.status = 'running'
        item.save()
        send_mail(item)
        item.status = 'completed'
        item.save()


def monthly_send():
    for item in Mail.objects.filter(frequency='monthly'):
        item.status = 'running'
        item.save()
        send_mail(item)
        item.status = 'completed'
        item.save()


def mail_send(message_item: Mail):
    # Получаем список email-адресов клиентов, которым нужно отправить рассылку
    client_emails = message_item.client.values_list('email', flat=True)  # noqa(отключить проверку)

    # Отправляем письмо каждому клиенту
    for email in client_emails:
        message = Message.objects.create(mail_settings=message_item)
        try:
            send_mail(
                message_item.subject,  # Тема письма
                message_item.body,  # Тело письма
                settings.EMAIL_HOST_USER,  # От кого отправляем письмо
                [email],  # Кому отправляем письмо
                fail_silently=False,
            )
            status = 'success'
            response = 'Email sent successfully'
        except Exception as e:
            status = 'error'
            response = str(e)
        Log.objects.create(message=message, status=status, response=response)


def get_cached_log_data(log):
    if settings.CACHE_ENABLE:
        cache_key = f'log_{log.pk}'
        cached_data = cache.get(cache_key)
        if cached_data is None:
            cached_data = {
                'message': log.message,  # Сообщение для рассылки
                'timestamp': log.timestamp,  # Дата и время последней попытки
                'status': log.status,  # Статус попытки
                'response': log.response,  # Ответ почтового сервера, если он был
            }
            cache.set(cache_key, cached_data, 300)  # Кешируем данные на 5 минут
        return cached_data
    else:
        return {
            'message': log.message,  # Сообщение для рассылки
            'timestamp': log.timestamp,  # Дата и время последней попытки
            'status': log.status,  # Статус попытки
            'response': log.response,  # Ответ почтового сервера, если он был
        }
