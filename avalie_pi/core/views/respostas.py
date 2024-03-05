from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from django.utils import timezone

from core.models import Respostas
from core.serializer import RespostasSerializer
from core.usecases.respostas import CaseRespostas
from configs.permissions import perm
from core.models import Avaliacao

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

class RespostasViewSet(viewsets.ModelViewSet):

    permission_classes = []
    queryset = Respostas.objects.all()
    serializer_class = RespostasSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    pagination_class = CustomPageNumberPagination
    
    search_fields = [
        'id_avaliacao',
    ]
    
    def get_serializer_class(self):
        actions = [
            'create',
            'update',
            'partial_update'
        ]

        if self.action in actions:
            return RespostasSerializer
        return self.serializer_class

    def put(self, request, id=None):

        _data = Respostas.objects.filter(id=id)
        serializer = RespostasSerializer(_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='list_all')
    def list_all(self, request):

        try:
            data = CaseRespostas.list_all()

            return Response(data=data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'], url_path='avaliacao')
    def response_asseessment(self, request):
        """ 
        API de resposta da avaliação 
        
        ```json
        [
            {
                "cpf": number,
                "id_avaliacao": number,
                "survey_id": number,
                "question_id": number,
                "option_id": number,
                "texto_resposta": string
            }
        ]
        """
        
        try:
            respostas = request.data

            for resposta in respostas:
                
                    is_response = Respostas.objects.filter(id_avaliacao=resposta["id_avaliacao"])
                    if is_response:
                        return Response(data={"formulario ja respondido"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    response = Respostas(id_avaliacao=resposta['id_avaliacao'],
                            survey_id=resposta['survey_id'],
                            question_id=resposta['question_id'],
                            option_id=resposta['option_id'],
                            texto_resposta=resposta['texto_resposta'],
                            criado_em=datetime.now()
                    )
                    response.save()

                    avaliacao_obj = Avaliacao.objects.filter(hash=resposta['id_avaliacao']).first()
                    if avaliacao_obj:
                        avaliacao_obj.respondido_em = timezone.now()
                        avaliacao_obj.save()


            return Response(data={"recorded_response": True}, status=status.HTTP_200_OK)

        except Exception as err:
            print("erro..:", err)
            return Response(data={"recorded_response": False}, status=status.HTTP_400_BAD_REQUEST)

        
