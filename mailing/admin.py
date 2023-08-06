from django.contrib import admin

from mailing.models import Client, Mail, Message, Log


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    list_filter = ('email', 'full_name', 'comment')
    search_fields = ('email', 'full_name')


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body', 'periodicity', 'status')
    list_filter = ('periodicity', 'status')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'body', 'mail_settings',)
    list_filter = ('theme',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('message', 'timestamp', 'status')
    list_filter = ('message', 'timestamp', 'status')
    search_fields = ('message', 'timestamp', 'status')
