from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from core.models import CanalPrestacao
from core.serializer import CanalPrestacaoSerializer
from configs.permissions import perm

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    
class CanalPrestacaoViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated, perm('IsCanalPrestacao')]
    pagination_class = CustomPageNumberPagination
    queryset = CanalPrestacao.objects.all()
    serializer_class = CanalPrestacaoSerializer
    filter_backends = (SearchFilter, OrderingFilter)

    search_fields = [
        'id',
    ]

    def get_serializer_class(self):
        actions = [
            'create',
            'update',
            'partial_update'
        ]

        if self.action in actions:
            return CanalPrestacaoSerializer
        return self.serializer_class

    def put(self, request, id=None):

        _data = CanalPrestacao.objects.filter(id=id)
        serializer = CanalPrestacaoSerializer(_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

