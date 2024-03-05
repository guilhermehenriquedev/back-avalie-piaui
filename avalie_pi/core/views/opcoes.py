from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from core.models import Opcoes
from core.serializer import OpcoesSerializer
from configs.permissions import perm


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class OpcoesViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, perm('IsOpcoes')]
    queryset = Opcoes.objects.all()
    serializer_class = OpcoesSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    pagination_class = CustomPageNumberPagination
    
    search_fields = [
        'option_id',
    ]
    
    def get_serializer_class(self):
        actions = [
            'create',
            'update',
            'partial_update'
        ]

        if self.action in actions:
            return OpcoesSerializer
        return self.serializer_class

    def put(self, request, id=None):

        _data = Opcoes.objects.filter(id=id)
        serializer = OpcoesSerializer(_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)