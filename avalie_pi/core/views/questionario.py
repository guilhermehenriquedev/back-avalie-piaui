from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.db.models import Subquery, OuterRef

from core.usecases.questionario import Questionario
from core.models import Pesquisas,TipoService, Orgao
from core.serializer import PesquisasSerializer
from configs.permissions import perm
import json

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    
class QuestionarioViewSet(viewsets.ModelViewSet):    

    '''
    Para busca personalizada, coloque na url os seguintes parametros (titulo, ativo, tipo_servico)
    
    ```link
    /Questionario/?page_size=100&titulo=qualquer_nome&ativo=1_ou_0&tipo_servico=qualquer_nome
    
    '''
    permission_classes = [IsAuthenticated, perm('IsQuestionarios')]
    queryset = Pesquisas.objects.all()
    serializer_class = PesquisasSerializer
    pagination_class = CustomPageNumberPagination
    
    def format_data_with_names(self, data):
        formatted_data = []
        for item in data:
            orgao_id = item.pop('orgao_id', None)
            tipo_service_id = item.pop('tipo_servico', None)

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
        
        titulo = self.request.query_params.get('titulo', None)
        ativo = self.request.query_params.get('ativo', None)
        tipo_servico = self.request.query_params.get('tipo_servico', None)

        queryset = Pesquisas.objects.all()

        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)

        if ativo:
            queryset = queryset.filter(is_active=ativo)
        
        if tipo_servico:
            subquery = TipoService.objects.filter(id=OuterRef('tipo_servico')).values('nome')[:1]
            queryset = queryset.annotate(orgao_nome=Subquery(subquery)).filter(orgao_nome__icontains=tipo_servico)

        return queryset
    
    def list(self, request):
        
        page_size = request.query_params.get('page_size', None)
        
        queryset = self.get_queryset()
        
        if page_size:
            paginator = CustomPageNumberPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = PesquisasSerializer(paginated_queryset, many=True)
            
            formatted_data = self.format_data_with_names(serializer.data)
            
            data = {
                'count': paginator.page.paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': formatted_data,
            }
        else:
            serializer = PesquisasSerializer(queryset, many=True)
            data = self.format_data_with_names(serializer.data)

        return Response(data, status=status.HTTP_200_OK)
        

    @action(detail=False, methods=['post'], url_path='create')
    def form_create(self, request):
        ''' 
            Cria questionario de avaliacao 
            
            Payload para requisição POST:
            ```json
            {
                "orgao_id": number,
                "titulo": string,
                "descricao": string,
                "user_id": number,
                "tipo_servico": number,
                "dict_perguntas": [
                    {
                        "texto_pergunta": string, 
                        "tipo_pergunta": number, 
                        "opcoes": []
                    }
                ],
            }
            
        '''

        try:
            
            request_body = request.body
            data = json.loads(request_body)
            
            
            orgao_id = data.get("orgao_id", None)
            titulo = data.get("titulo", None)
            descricao = data.get("descricao", None)
            user_id = data.get("user_id", None)
            tipo_servico = data.get("tipo_servico", None)
            dict_perguntas = data.get("dict_perguntas", [])

            create_questionarie = Questionario.create(title=titulo, 
                                                        description=descricao, 
                                                        orgao=orgao_id, 
                                                        user_id=user_id, 
                                                        tipo_servico=tipo_servico, 
                                                        dict_perguntas=dict_perguntas)
            
            return Response(data={'created': True}, status=status.HTTP_201_CREATED)

        except Exception as err:
            print(err)
            return Response(data={'created': False}, status=status.HTTP_400_BAD_REQUEST)