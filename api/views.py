from django.shortcuts import render
from django.http import Http404
from record.models import Sheet, Category
from .serializers import SheetSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly

from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse

# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'sheets': reverse('sheet-list', request=request, format=format),
    })

class SheetViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]