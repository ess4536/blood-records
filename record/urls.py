from django.urls import path
from . import views

# Create your rooting here.
app_name = 'record'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('record-list/', views.RecordListView.as_view(), name="record_list"),
    path('record-detail/', views.RecordDetailView.as_view(), name="record_detail"),
    path('record-detail/<int:pk>/', views.RecordDetailNextView, name="record_detail_next"),
    path('record-create/', views.RecordCreateView.as_view(), name="record_create"),
    path('record-update/<int:pk>/', views.RecordUpdateView.as_view(), name="record_update"),
    path('record-delete/<int:pk>/', views.RecordDeleteView.as_view(), name="record_delete"),
    path('category-create/', views.CategoryCreateView.as_view(), name="category_create"),
    path('category-update/<int:pk>', views.CategoryUpdateView.as_view(), name="category_update"),
    path('category-delete/<int:pk>', views.CategoryDeleteView.as_view(), name="category_delete"),
    path('sheet-create/', views.SheetCreateView.as_view(), name="sheet_create"),
    path('sheet-update/<int:pk>', views.SheetUpdateView.as_view(), name="sheet_update"),
    path('sheet-delete/<int:pk>/', views.SheetDeleteView.as_view(), name="sheet_delete"),
    path('follow/<slug:username>/', views.FollowView, name="follow"),
    path('unfollow/<slug:username>/', views.UnfollowView, name="unfollow"),
    path('approval/<slug:username>/', views.ApprovalView.as_view(), name="approval"),
]

