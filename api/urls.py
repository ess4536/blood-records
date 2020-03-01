from django.urls import path, include
from . import views

from rest_framework.urlpatterns import format_suffix_patterns

# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'sheet', views.SheetViewSet)

app_name = 'api'
urlpatterns = [
    path('sheet/', views.SheetList.as_view(), name="sheet_list"),
    path('sheet/<int:pk>/', views.SheetDetail.as_view(), name="sheet_detail"),
    # path('', include(router.urls)),
    # path('api/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
