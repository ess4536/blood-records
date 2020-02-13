import logging
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Q
from .forms import InquiryForm, RecordCreateForm, CategoryCreateForm, SheetCreateForm
from .models import Record, Category, Sheet
from accounts.models import CustomUser, Relationship
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
    model = Record, CustomUser, Relationship
    template_name = 'record_list.html'

    def get(self, request, *args, **kwargs):
        queryset = Record.objects.filter(user=self.request.user).order_by('category')
        record = queryset.order_by('date')
        date = Record.objects.filter(user=self.request.user).values_list('date', flat=True).order_by('date').distinct()
        cate_list = Category.objects.filter(user=self.request.user)
        sheet_list = Sheet.objects.filter(user=self.request.user)
        relation_list = Relationship.objects.filter(user=self.request.user)
        follow = Relationship.objects.filter(user=self.request.user).values_list('follow',flat=True )

        if follow:
            for follow in follow:
                follow_record = Record.objects.filter(user=follow).order_by('date')
                follow_cate = Category.objects.filter(user=follow)
                follow_date = Record.objects.filter(user=follow).values_list('date', flat=True).order_by('date').distinct()
        else:
            follow_record = ""
            follow_cate = ""
            follow_date = ""

        q_word = self.request.GET.get('query')

        if q_word:
            object_list = CustomUser.objects.filter(Q(username__icontains=q_word))
        else:
            object_list = CustomUser.objects.all()
        
        context = {
            'queryset': queryset,
            'record': record,
            'date': date,
            'cate_list': cate_list,
            'sheet_list': sheet_list,
            'relation_list': relation_list,
            'follow_record': follow_record,
            'follow_cate': follow_cate,
            'follow_date': follow_date,
            'object_list': object_list,
        }
        return render(request, 'record_list.html', context)

class RecordDetailView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'record_detail.html'

    def get(self, request, *args, **kwargs):
        category_list = Category.objects.filter(user=self.request.user)
        sheet_list = Sheet.objects.filter(user=request.user)
        context = {
            'category_list': category_list,
            'sheet_list': sheet_list,
        }
        return render(request, 'record_detail.html', context)

def RecordDetailNextView(request, pk):
    record_list = Record.objects.filter(user=request.user, category=pk).order_by('-date')
    context = {
        'record_list': record_list
        }
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
        category.user = self.request.user
        category.save()
        messages.success(self.request, 'カテゴリを作成しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'カテゴリの作成に失敗しました')
        return super().form_invalid(form)

class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    template_name = 'category_update.html'
    form_class = CategoryCreateForm

    def get_success_url(self):
        return reverse_lazy('record:record_list')

    def form_valid(self, form):
        messages.success(self.request, 'カテゴリーを更新しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'カテゴリーの更新に失敗しました')
        return super().form_invalid(form)

class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('record:record_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'カテゴリーを削除しました')
        return super().delete(request, *args, **kwargs)

class SheetCreateView(LoginRequiredMixin, generic.CreateView):
    model = Sheet
    template_name = 'sheet_create.html'
    form_class = SheetCreateForm
    success_url = reverse_lazy('record:record_list')

    def form_valid(self, form):
        sheet = form.save(commit=False)
        sheet.user = self.request.user
        sheet.save()
        messages.success(self.request, 'シートを作成しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'シートの作成に失敗しました')
        return super().form_invalid(form)

class SheetUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Sheet
    template_name = 'sheet_update.html'
    form_class = SheetCreateForm

    def get_success_url(self):
        return reverse_lazy('record:record_list')

    def form_valid(self, form):
        messages.success(self.request, 'シートを更新しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'シートの更新に失敗しました')
        return super().form_invalid(form)

class SheetDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Sheet
    template_name = 'sheet_delete.html'
    success_url = reverse_lazy('record:record_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'シートを削除しました')
        return super().delete(request, *args, **kwargs)

class Share(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    template_name = 'share.html'

    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        q_word = self.request.GET.get('query')

        if q_word:
            object_list = CustomUser.objects.filter(Q(username__icontains=q_word))
        else:
            object_list = CustomUser.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(Share, self).get_context_data(**kwargs)
        username = self.kwargs['username']
        context['username'] = username
        context['follow'] = Relationship.objects.filter(user__username=username).count()
        context['user'] = Relationship.objects.filter(follow__username=username).count()

        if username is not self.request.user:
            result = Relationship.objects.filter(user__username=self.request.user).filter(follow__username=username)
            context['relation'] = True if result else False
        return context

def FollowView(request, *args, **kwargs):
    try:
        user = CustomUser.objects.get(username=request.user.username)
        follow = CustomUser.objects.get(username=kwargs['username'])
    except CustomUser.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
        return redirect('record:index')
    if user == follow:
        messages.warning(request, 'フォローできません')
    else:
        created = Relationship.objects.get_or_create(user=user, follow=follow)

        if (created):
            messages.success(request, 'フォローしました')
        else:
            messages.warning(request, 'すでにフォローしています')
    return redirect('record:record_list')

def UnfollowView(request, *args, **kwargs):
    try:
        user = CustomUser.objects.get(username=request.user)
        follow = CustomUser.objects.get(username=kwargs['username'])
        if user == follow:
            messages.warning(request, '自分自身のフォローを外せません')
        else:
            unfollow = Relationship.objects.get(user=user, follow=follow)
            unfollow.delete()
            messages.success(request, 'あなたは{}のフォローを外しました'.format(user.username))
    except CustomUser.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['username']))
    except Relationship.DoesNotExist:
        messages.warning(request, 'あなたは{0}をフォローしませんでした'.format(user.username))
    return redirect('record:record_list')
