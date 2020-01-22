import logging
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm
from .models import Record
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

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


class RecordListView(LoginRequiredMixin, generic.ListView):
    model = Record
    Template_name = 'record_list.html'

    def get_queryset(self):
        records = Record.objects.fillter(user=self.request.user).order_by('-create_at')
        return records