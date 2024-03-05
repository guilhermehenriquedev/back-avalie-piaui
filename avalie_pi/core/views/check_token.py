import jwt

from datetime import datetime, timezone
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from configs.settings import SECRET_KEY
from core.usecases.token import renovar_token


class TokenValidationViewSet(viewsets.ViewSet):
    
    permission_classes = [] 
    
    @action(detail=False, methods=['post'], url_path='token')
    def verify_token(self, request):
        '''
            Responsável por verificar a validade do token e fazer tratativa de troca de acesso
            
            Payload para requisição POST
            ```json
            {
                "token_acess": string,
                "token_refresh": string
            }
        '''
        token_access = request.data.get('token_access', '')
        token_refresh = request.data.get('token_refresh', '')
        try:
            # Decodifica o token
            payload = jwt.decode(token_access, SECRET_KEY, algorithms=['HS256'])

            expiracao = payload.get('exp', 0)
            emissao = payload.get('iat', 0)

            agora = datetime.utcnow().replace(tzinfo=timezone.utc)
            expiracao_dt = datetime.utcfromtimestamp(expiracao).replace(tzinfo=timezone.utc)
            emissao_dt = datetime.utcfromtimestamp(emissao).replace(tzinfo=timezone.utc)

            if agora < expiracao_dt:
                return Response(data={"is_valid": True}, status=status.HTTP_200_OK)
            else:
                novo_token_acesso, novo_token_refresh = renovar_token(token_refresh)
                return Response(data={"is_valid": False, "new_access": novo_token_acesso, "new_refresh": novo_token_refresh}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.ExpiredSignatureError:
            novo_token_acesso, novo_token_refresh = renovar_token(token_refresh)
            return Response(data={"is_valid": False, "new_access": novo_token_acesso, "new_refresh": novo_token_refresh}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            novo_token_acesso, novo_token_refresh = renovar_token(token_refresh)
            return Response(data={"is_valid": False, "new_access": novo_token_acesso, "new_refresh": novo_token_refresh}, status=status.HTTP_400_BAD_REQUEST)
