#importacoes do django
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from core.models import Webhook
from core.serializer import WebhookSerializer
from configs.permissions import perm

class WebhookViewSet(viewsets.ModelViewSet):
    '''
        Api para Webhooks de envio do formulário e respostas
    '''
    permission_classes = [IsAuthenticated, perm('IsWebhook')]
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    filter_backends = (SearchFilter, OrderingFilter)

    search_fields = [
        'hash',
    ]
    
    def get_serializer_class(self):
        actions = [ 
            'create',
            'update',
            'partial_update',
            'delete'
        ]

        if self.action in actions:
            return WebhookSerializer
        return self.serializer_class

    def put(self, request, id=None):

        _data = Webhook.objects.filter(id=id)
        serializer = WebhookSerializer(_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard_webhook(self, request):
        pass