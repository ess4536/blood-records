from django.urls import path
from . import views

# Create your rooting here.
app_name = 'record'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('record-list', views.RecordListView.as_view(), name="record_list")
]

