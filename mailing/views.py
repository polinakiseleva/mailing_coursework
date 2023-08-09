from django.contrib.auth.decorators import login_required
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
    permission_required = 'mailing.add_client'

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
    permission_required = 'mailing.change_client'
    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование клиента'

        return context_data


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    permission_required = 'mailing.view_client'

    # extra_context = {'title': 'Список клиентов', }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список клиентов'

        return context_data


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = 'mailing.view_client'
    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Просмотр клиента'

        return context_data


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = 'mailing.delete_client'
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')

    # extra_context = {'title': 'Удаление клиента', }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление клиента'

        return context_data


class MailCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mail
    form_class = MailForm
    permission_required = 'mailing.add_mail'
    success_url = reverse_lazy('mailing:mail_list')

    def form_valid(self, form):
        form.instance.status = 'running'
        response = super().form_valid(form)
        mail_send(self.object)
        return response


class MailListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mail
    permission_required = 'mailing.view_mail'

    extra_context = {
        'title': 'Список рассылок'
    }


class MailDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mail
    permission_required = 'mailing.view_mail'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Просмотр рассылки'

        return context_data


class MailUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mail
    form_class = MailForm
    permission_required = 'mailing.change_mail'
    success_url = reverse_lazy('main:mail_list')
    template_name = 'mailing/mail_form.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Редактирование рассылки'

        return context_data


class MailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mail
    success_url = reverse_lazy('mailing:mail_list')
    permission_required = 'mailing.delete_mail'
    template_name = 'mailing/mail_confirm_delete.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Удаление рассылки'

        return context_data


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing.add_message'
    success_url = reverse_lazy('mailing:message_list')


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    permission_required = 'mailing.view_message'
    extra_context = {
        'title': 'Список сообщений'
    }


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    permission_required = 'mailing.change_message'
    success_url = reverse_lazy('mailing:message_list')


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailing.view_message'
    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Просмотр сообщения'

        return context_data


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    permission_required = 'mailing.delete_message'
    template_name = 'mailing/message_confirm_delete.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Удаление рассылки'


@login_required
def index(request):
    all_mail = Mail.objects.all().count()
    active_mail = Mail.objects.filter(status='running').count()
    all_client = Client.objects.all().count()
    articles_model = Blog.objects.all().order_by('?')[:3]
    context = {
        'all_mail': all_mail,
        'all_client': all_client,
        'active_mail': active_mail,
        'article_object_list': articles_model,
        'title': 'Главная'
    }
    return render(request, 'mailing/home.html', context)


@login_required
def contact_inf(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mailing/contact_inf.html', context)
