from django.shortcuts import render
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from record.models import Sheet
from .serializers import SheetSerializer

from rest_framework import generics
from rest_framework import permissions

# Create your views here.

class SheetList(generics.ListCreateAPIView):
    """ List all sheet, or create a new sheet. """

    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SheetDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve, update or delete a sheet. """

    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]