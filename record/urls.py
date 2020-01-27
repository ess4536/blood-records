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
]

