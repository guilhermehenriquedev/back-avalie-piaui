#importacoes para funcinalidades
import uuid
import datetime
#importacoes do django
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
#importacoes do projeto
from core.models import Avaliacao, WebhookRuntime
from core.serializer import AvaliacaoSerializer
from core.usecases.avaliacao import CaseAvaliacao
from core.usecases.webhook import CaseWebhook
from configs.permissions import perm
from rest_framework.pagination import PageNumberPagination

from datetime import datetime

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class AvaliacaoViewSet(viewsets.ModelViewSet):

    permission_classes = []
    pagination_class = CustomPageNumberPagination
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    filter_backends = (SearchFilter, OrderingFilter)

    search_fields = [
        'hash',
    ]
    
    def get_serializer_class(self):
        actions = [ 
            'create',
            'update',
            'partial_update'
        ]

        if self.action in actions:
            return AvaliacaoSerializer
        return self.serializer_class

    def put(self, request, id=None):

        _data = Avaliacao.objects.filter(id=id)
        serializer = AvaliacaoSerializer(_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='create')
    def create_assessment(self, request):
        
        """ 
        Cria a avaliação retornando a hash
        
        Modelo para requisição POST
        ```json
        {
            "idService": number,
            "idOrgao": number,
            "cpf": number,
            "protocolo": string,
            "idCanalPrestacao": number,
            "idCanalAvaliacao": number,
            "idPesquisa": number,
            "nome": string,
            "telefone": string,
            "email": string
        }
        """
        try:
            data = request.data
            _uuid = uuid.uuid4() #gera uma hash aleatória
            
            assessment = Avaliacao(hash=_uuid, 
                                    idService=data["idService"],
                                    idOrgao=data["idOrgao"],
                                    cpf=data["cpf"],
                                    nome=data['nome'],
                                    telefone=data['telefone'],
                                    email=data['email'],
                                    protocolo=data["protocolo"],
                                    idPesquisa=data["idPesquisa"],
                                    criado_em=datetime.now()
                                   )
            assessment.save()
            
            data["type_webhook"] = 2 #ASSESSMENT_CREATE 
            send_webhook = CaseWebhook.send_event_assessment(data=data, hash=_uuid)
            
            send_runtime_webhook = WebhookRuntime(
                type=data["type_webhook"],
                status_code=send_webhook["status"],
                date=datetime.now(),
                runtime=send_webhook["runtime"]
            )
            send_runtime_webhook.save()
            
            return Response(data={'assessment_created': True, "hash": assessment.hash}, status=status.HTTP_201_CREATED)
            
        except Exception as err:
            print("erro...", err)
            return Response(data={'assessment_created': False}, status=status.HTTP_400_BAD_REQUEST)
            
    @action(detail=False, methods=['get'], url_path='get_assessment')
    def get_assesment(self, request):
        """ 
        Retorna os dados da avaliação pela hash 
        
        Informe como parametro na url a hash da avaliação da seguinte forma:
        ```link
        api/Avaliacao/get_assessment/?hash=a3457f63-574e-4b4f-923a-d74c9fdb8fd9
        """
    
        try:

            _hash = request.GET.get('hash')
            
            data = CaseAvaliacao.get_assessment(hash=_hash)
            return Response(data, status=status.HTTP_200_OK)

        except Exception as err:
            print(err)
    
    @action(detail=False, methods=['get'], url_path='list_all')
    def list_all(self, request):
        '''
            Lista todas as avaliações feitas, com os nomes formatados pelos ids
            
            Método de requisição: GET
        '''
        try:
            
            data = CaseAvaliacao.list()
            return Response(data, status=status.HTTP_200_OK)

        except Exception as err:
            print(err)