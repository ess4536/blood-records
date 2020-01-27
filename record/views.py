import logging
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm, RecordCreateForm
from .models import Record, Category
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
    template_name = 'record_list.html'

    def get_queryset(self):
        queryset = Record.objects.filter(user=self.request.user).order_by('date')
        return queryset

class RecordDetailView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'record_detail.html'

def RecordDetailNextView(request, pk):
    record_list = Record.objects.filter(category=pk).order_by('-date')
    context = {'record_list': record_list}
    return render(request, 'record_detail_next.html', context)

class RecordCreateView(LoginRequiredMixin, generic.CreateView):
    model = Record
    template_name = 'record_create.html'
    form_class = RecordCreateForm
    success_url = reverse_lazy('record:record_list')

    def form_valid(self, form):
        record = form.save(commit=False)
        record.user = self.request.user
        record.save()
        messages.success(self.request, '記録を作成しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "記録の作成に失敗しました")
        return super().form_invalid(form)