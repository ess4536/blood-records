import logging
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm, RecordCreateForm, CategoryCreateForm
from .models import Record, Category
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model
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

    def get(self, request, *args, **kwargs):
        queryset = Record.objects.filter(user=self.request.user).order_by('category')
        date = Record.objects.values_list('date', flat=True).order_by('date').distinct()
        cate_name = Category.objects.values_list('name', flat=True).distinct()
        context = {
            'queryset': queryset,
            'date': date,
            'cate_name': cate_name,
        }
        return render(request, 'record_list.html', context)

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

class RecordUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Record
    template_name = 'record_update.html'
    form_class = RecordCreateForm

    def get_success_url(self):
        return reverse_lazy('record:record_list')

    def form_valid(self, form):
        messages.success(self.request, '記録を更新しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, '記録の更新に失敗しました')
        return super().form_invalid(form)

class RecordDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Record
    template_name = 'record_delete.html'
    success_url = reverse_lazy('record:record_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '記録を削除しました')
        return super().delete(request, *args, **kwargs)

class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    template_name = 'category_create.html'
    form_class = CategoryCreateForm
    success_url = reverse_lazy('record:record_list')

    def form_valid(self, form):
        category = form.save(commit=False)
        category.save()
        messages.success(self.request, 'カテゴリを作成しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'カテゴリの作成に失敗しました')
        return super().form_invalid(form)
