from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import ClientCreateView, ClientUpdateView, ClientListView, \
    MailCreateView, MailDetailView, MailUpdateView, MailListView, MailDeleteView, index, ClientDetailView, \
    ClientDeleteView, contact_inf, MessageCreateView, MessageListView, MessageDetailView, MessageUpdateView, \
    MessageDeleteView

app_name = MailingConfig.name
urlpatterns = [
    path('', cache_page(60)(index), name='home'),
    path('contacts/', contact_inf, name='contacts'),

    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/client_update/', ClientUpdateView.as_view(), name='client_update'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('<int:pk>/client_view/', ClientDetailView.as_view(), name='client_view'),
    path('<int:pk>/client_delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('mail_create/', MailCreateView.as_view(), name='mail_create'),
    path('<int:pk>/mail_update/', MailUpdateView.as_view(), name='mail_update'),
    path('mail/', MailListView.as_view(), name='mail_list'),
    path('<int:pk>/mail_view/', MailDetailView.as_view(), name='mail_view'),
    path('<int:pk>/mail_delete/', MailDeleteView.as_view(), name='mail_delete'),

    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('<int:pk>/message_view/', MessageDetailView.as_view(), name='message_view'),
    path('<int:pk>/message_update/', MessageUpdateView.as_view(), name='message_update'),
    path('<int:pk>/message_delete/', MessageDeleteView.as_view(), name='message_delete'),

]
