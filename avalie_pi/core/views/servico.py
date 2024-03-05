from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from core.models import Servico, Orgao, TipoService
from core.serializer import ServicoSerializer
from configs.permissions import perm

from django.db.models import Subquery, OuterRef


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class ServicoViewSet(viewsets.ModelViewSet):

    '''
    Para busca personalizada, coloque na url os seguintes parametros (nome, ativo, orga0)
    
    ```link
    /Servico/?ativo=1_ou_0&nome=qualquer_nome&orgao=qualquer_nome
    
    '''
    
    permission_classes = [IsAuthenticated, perm('IsServico')]
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    pagination_class = CustomPageNumberPagination

    search_fields = [
        'response_id',
    ]

    def get_serializer_class(self):
        actions = ['create', 'update', 'partial_update', 'delete']

        if self.action in actions:
            return ServicoSerializer
        return self.serializer_class

    def put(self, request, id=None):
        _data = Servico.objects.filter(id=id)
        serializer = ServicoSerializer(_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        # Obtém o parâmetro de paginação 'page_size' da solicitação
        page_size = request.query_params.get('page_size', None)

        queryset = self.get_queryset()

        if page_size:
            paginator = CustomPageNumberPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = ServicoSerializer(paginated_queryset, many=True)

            formatted_data = self.format_data_with_names(serializer.data)

            data = {
                'count': paginator.page.paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': formatted_data,
            }
        else:
            serializer = ServicoSerializer(queryset, many=True)
            data = self.format_data_with_names(serializer.data)

        return Response(data, status=status.HTTP_200_OK)

    def format_data_with_names(self, data):
        formatted_data = []
        for item in data:
            orgao_id = item.pop('idOrgao', None)
            tipo_service_id = item.pop('id_tipoService', None)

            if orgao_id:
                try:
                    orgao = Orgao.objects.get(id=orgao_id)
                    item['orgao'] = orgao.nome
                    item['id_orgao'] = orgao.id
                except Orgao.DoesNotExist:
                    item['orgao'] = None
                    item['id_orgao'] = None

            if tipo_service_id:
                try:
                    tipo_service = TipoService.objects.get(id=tipo_service_id)
                    item['tipo_servico'] = tipo_service.nome
                    item['id_tipoService'] = tipo_service.id
                except TipoService.DoesNotExist:
                    item['tipo_servico'] = None
                    item['id_tipoService'] = None

            formatted_data.append(item)

        return formatted_data
    

    def get_queryset(self):
        
        #aplica os filtros
        nome = self.request.query_params.get('nome', None)
        ativo = self.request.query_params.get('ativo', None)
        orgao = self.request.query_params.get('orgao', None)

        queryset = Servico.objects.all()

        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        if ativo:
            queryset = queryset.filter(ativo=ativo)
            
        if orgao:
            subquery = Orgao.objects.filter(id=OuterRef('idOrgao')).values('nome')[:1]
            queryset = queryset.annotate(orgao_nome=Subquery(subquery)).filter(orgao_nome__icontains=orgao)

        return queryset


