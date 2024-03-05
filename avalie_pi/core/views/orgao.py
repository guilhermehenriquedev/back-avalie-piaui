from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from core.models import Orgao
from core.serializer import OrgaoSerializer
from configs.permissions import perm


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrgaoViewSet(viewsets.ModelViewSet):
    
    '''
    Para busca personalizada, coloque na url os seguintes parametros, o nome_curto pode ser qualquer letra que fara a busca
    
    ```link
    /orgaos/?nome_curto=sead&ativo=0
    
    '''
    
    permission_classes = [IsAuthenticated, perm('IsOrgao')]
    queryset = Orgao.objects.all()
    serializer_class = OrgaoSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    pagination_class = CustomPageNumberPagination  # Utiliza a custom pagination class
    
    search_fields = [
        'id',
        'nome_curto',
        'ativo'
    ]

    def get_serializer_class(self):
        actions = ['create', 'update', 'partial_update']

        if self.action in actions:
            return OrgaoSerializer
        return self.serializer_class

    def put(self, request, id=None):
        _data = Orgao.objects.filter(id=id)
        serializer = OrgaoSerializer(_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get_queryset(self):
        
        queryset = Orgao.objects.all()

        nome_curto = self.request.query_params.get('nome_curto', None)
        if nome_curto:
            queryset = queryset.filter(nome_curto__icontains=nome_curto)

        ativo = self.request.query_params.get('ativo', None)
        if ativo:
            queryset = queryset.filter(ativo=ativo)

        return queryset

