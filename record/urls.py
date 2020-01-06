from django.urls import path
from . import views

# Create your rooting here.
app_name = 'record'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
]

