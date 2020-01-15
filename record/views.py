import logging
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm
from django.contrib import messages

# Create your views here.
logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('record:inquiry')

    def get_form(self, form_class=None):
        if 'name' in self.request.POST:
            form_data = self.request.POST
        else:
            form_data = self.request.session.get('form_data', None)
        return self.form_class(form_data)

    def from_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super(InquiryView, self).form_valid(form)