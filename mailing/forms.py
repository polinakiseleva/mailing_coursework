from django import forms

from mailing.models import Client, Mail, Message, Log


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_published":
                field.widget.attrs["class"] = "form-control"


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'email', 'comment']


class MailForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['subject', 'body', 'periodicity', 'status', 'client']


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = '__all__'
