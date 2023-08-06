from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Контактный email', unique=True)
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mail(models.Model):
    # периодичность рассылки
    PERIODICITY_OF_SENDING = (
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    )

    # статус рассылки
    MAILING_STATUSES = (
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    )

    subject = models.CharField(max_length=50, verbose_name='Тема рассылки')
    body = models.TextField(verbose_name='Содержание письма')
    periodicity = models.CharField(max_length=25, choices=PERIODICITY_OF_SENDING, verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=25, choices=MAILING_STATUSES, default='created',
                              verbose_name='Статус рассылки')
    client = models.ManyToManyField('Client', verbose_name='Клиенты', related_name='mail')

    def __str__(self):
        return f'{self.subject} - {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    theme = models.CharField(max_length=100, verbose_name='Тема письма', **NULLABLE)
    body = models.TextField(verbose_name='Тело письма', **NULLABLE)
    mail_settings = models.OneToOneField(Mail, verbose_name='Рассылка', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f"{self.theme}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Log(models.Model):
    # статус попытки
    STATUS_CHOICES = (
        ('success', 'Успешно'),
        ('error', 'Ошибка'),
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение для рассылки')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Последняя отправка')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, verbose_name='Статус попытки')
    response = models.TextField(verbose_name='Ответ почтового сервера')

    def __str__(self):
        return f"Время рассылки: {self.timestamp}\n"

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
        ordering = ["-timestamp"]
