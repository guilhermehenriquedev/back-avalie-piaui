from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from core.models import Pesquisas as PesquisaModel
from core.serializer import PesquisasSerializer
from core.usecases.pesquisas import Pesquisas
from configs.permissions import perm

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class PesquisasViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, perm('IsPesquisas')]
    queryset = PesquisaModel.objects.all()
    serializer_class = PesquisasSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    pagination_class = CustomPageNumberPagination
    
    search_fields = [
        'survey_id',
    ]
    
    def get_serializer_class(self):
        actions = [
            'create',
            'update',
            'partial_update'
        ]

        if self.action in actions:
            return PesquisasSerializer
        return self.serializer_class

    def put(self, request, id=None):

        _data = PesquisaModel.objects.filter(id=id)
        serializer = PesquisasSerializer(_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='get_per_id')
    def get_per_id(self, request):
        '''
            Busca a pesquisa pelo survey id
            
            Passe na url get o parametro do id:
            ```link
            /api/Pesquisas/get_per_id/?id=34
        '''
        try:

             _id = request.GET.get('id')
             data = Pesquisas.get_the_search(survey_id=_id)

             return Response(data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
            