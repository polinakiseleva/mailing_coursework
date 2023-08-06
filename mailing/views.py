from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from blog.models import Blog
from mailing.forms import ClientForm, MailForm, MessageForm
from mailing.models import Client, Mail, Message
from mailing.services import get_cached_log_data, mail_send


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    permission_required = 'mailing.client_create'

    # extra_context = {'title': 'Создание клиента', }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание клиента'

        return context_data

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailing.client_update'
    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Редактирование клиента'

        return context_data


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    permission_required = 'mailing.client_view'

    # extra_context = {'title': 'Список клиентов', }

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список клиентов'

        return context_data


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = 'mailing.client_view'
    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Просмотр клиента'

        return context_data


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = 'mailing.client_delete'
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')

    # extra_context = {'title': 'Удаление клиента', }

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Удаление клиента'

        return context_data


class MailCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mail
    form_class = MailForm
    permission_required = 'mailing.mail_create'
    success_url = reverse_lazy('mailing:mail_list')

    def form_valid(self, form):
        form.instance.status = 'running'
        response = super().form_valid(form)
        mail_send(self.object)
        return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        message_item = self.object
        message_item.status = 'running'
        message_item.save()
        mail_send(message_item)
        return response


class MailListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mail
    permission_required = 'mailing.mail_view'

    extra_context = {
        'title': 'Список рассылок'
    }


class MailDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mail
    permission_required = 'mailing.mail_view'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Просмотр рассылки'

        return context_data


class MailUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mail
    form_class = MailForm
    permission_required = 'mailing.mail_update'
    success_url = reverse_lazy('main:mail_list')
    template_name = 'mailing/mail_form.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Редактирование рассылки'

        return context_data


class MailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mail
    success_url = reverse_lazy('mailing:mail_list')
    permission_required = 'mailing.mail_delete'
    template_name = 'mailing/mail_confirm_delete.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Удаление рассылки'

        return context_data


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing.message_create'
    success_url = reverse_lazy('mailing:message_list')


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    permission_required = 'mailing.message_create'
    extra_context = {
        'title': 'Список сообщений'
    }


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    permission_required = 'mailing.message_update'
    success_url = reverse_lazy('mailing:message_list')


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing.message_view'
    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Просмотр сообщения'

        return context_data


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    permission_required = 'mailing.message_delete'
    template_name = 'mailing/message_confirm_delete.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Удаление рассылки'


def index(request):
    """
    Функция отображения главной страницы
    """
    context = {
        'all_mail': Mail.objects.all().count(),
        'all_clients': Client.objects.all().count(),
        'article_object_list': Blog.objects.all().order_by('?')[:3],
        'title': 'Главная'
    }
    return render(request, 'mailing/home.html', context)


def contact_inf(request):
    context = {
        'title': 'Contacts',
    }
    return render(request, 'mailing/contact_inf.html', context)
