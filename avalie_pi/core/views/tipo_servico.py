from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from core.models import TipoService
from core.serializer import TipoServiceSerializer
from configs.permissions import perm

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class TipoServiceViewSet(viewsets.ModelViewSet):

    '''
    Para busca personalizada, coloque na url os seguintes parametros, o nome pode ser qualquer letra que fara a busca
    
    ```link
    /TipoServico/?nome=sead&ativo=0
    
    '''
    permission_classes = [IsAuthenticated, perm('IsTipoServico')]
    queryset = TipoService.objects.all()
    serializer_class = TipoServiceSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    pagination_class = CustomPageNumberPagination
    
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
            return TipoServiceSerializer
        return self.serializer_class

    def put(self, request, id=None):

        _data = TipoService.objects.filter(id=id)
        serializer = TipoServiceSerializer(_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def get_queryset(self):
        
        queryset = TipoService.objects.all()

        nome = self.request.query_params.get('nome', None)
        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        ativo = self.request.query_params.get('ativo', None)
        if ativo:
            queryset = queryset.filter(ativo=ativo)

        return queryset