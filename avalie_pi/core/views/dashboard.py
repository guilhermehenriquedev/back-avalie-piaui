import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Sum

from configs.permissions import perm
from core.models import *
from core.serializer import *

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class Dashboard(viewsets.ViewSet):

    ''' Permissoes de status '''
    permission_classes = [IsAuthenticated, perm('IsDashboard')]

    @action(detail=False, methods=['get'], url_path='avalie')
    def dashboard_avalie(self, request):
        
        ''' View de dashboard, nps avalie '''
        db_respostas = Respostas.objects.all()
        total_respostas = len(db_respostas)
        
        respostas_serialzer =  RespostasSerializer(db_respostas, many=True)
        total_avaliacoes = Avaliacao.objects.count()
        
        avaliacoes_com_respostas = Avaliacao.objects.all()
        
        #NPS -------------------------
        soma_respostas = db_respostas.aggregate(soma_total=Sum('texto_resposta', output_field=models.IntegerField()))['soma_total']

        detratores = sum(int(reg.texto_resposta) for reg in db_respostas.filter(texto_resposta__in=["1", "2"]))
        passivos = sum(int(reg.texto_resposta) for reg in db_respostas.filter(texto_resposta="3"))
        promotores = sum(int(reg.texto_resposta) for reg in db_respostas.filter(texto_resposta__in=["4", "5"]))
        
        porcetagem_promotores = ((promotores - detratores) / soma_respostas) * 100
        porcetagem_detratores = ((detratores - detratores) / soma_respostas) * 100
        nps = porcetagem_promotores - porcetagem_detratores

        #calculo de taxa de respostas
        taxa_resposta = (total_respostas / total_avaliacoes) * 100

        # calculo orgaos avaliados
        quantidade_orgao_avaliados = avaliacoes_com_respostas.values('idOrgao').annotate(num=Count('idOrgao')).count()
        orgaos_avaliados = quantidade_orgao_avaliados

        #calculo servicos avaliados
        quantidade_servicos_avaliados = avaliacoes_com_respostas.values('idService').annotate(num=Count('idService')).count()
        servicos_avaliados = quantidade_servicos_avaliados
        
        #grafico nps
        data_grafico = {
            "total_respostas": total_respostas,
            "1": round(db_respostas.filter(texto_resposta="1").count() / total_respostas * 100, 2),
            "2": round(db_respostas.filter(texto_resposta="2").count() / total_respostas * 100, 2),
            "3": round(db_respostas.filter(texto_resposta="3").count() / total_respostas * 100, 2),
            "4": round(db_respostas.filter(texto_resposta="4").count() / total_respostas * 100, 2),
            "5": round(db_respostas.filter(texto_resposta="5").count() / total_respostas * 100, 2)
        }
        
        data = {
            "nps": nps,
            "avaliacoes": total_avaliacoes,
            "servicos_avaliados": servicos_avaliados,
            "orgao_avaliados": orgaos_avaliados,
            "taxa_resposta": taxa_resposta,
            "grafico_nps": data_grafico,
            "rancking_respostas": [],
            "respostas": respostas_serialzer.data
        }
        
        return Response(data, status=status.HTTP_200_OK)