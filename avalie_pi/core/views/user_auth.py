import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from core.serializer import UserSerializer
from core.usecases import audit
from configs.permissions import perm
from configs.roles import AppsAdminRoles, PermissionsAdminRoles
from core.models import AuthUserOrgao, Orgao
from core.serializer import UserSerializer, AuthUserOrgaoSerializer

from rolepermissions.roles import assign_role
from rolepermissions.permissions import grant_permission, revoke_permission, available_perm_status

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class UserAuthViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, perm('IsUserAuth')] 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    @action(detail=True, methods=['put'], url_path='edit_user')
    def edit_user(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            data = request.data.copy()
            # Removendo o campo 'password' se estiver presente nos dados da solicitação
            if 'password' in data:
                del data['password']
            
            serializer = UserSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                # atualiza o registro de orgao do usuario
                user_orgao = AuthUserOrgao.objects.get(id_user=pk)
                user_orgao.id_orgao = data['orgao']
                user_orgao.save()
                
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        except User.DoesNotExist:
            return Response(data='usuario nao existe', status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def authenticate_user(self, request):
        '''
        Autentica o usuario no banco de dados Django
        
        Modelo de requisição POST:
        ```json
        {
            "email": string,
            "password": string
        }
        '''
        email = request.data.get('email') 
        password = request.data.get('password')
        ip_usuario = request.META.get('REMOTE_ADDR')
        
        try:
            user = User.objects.select_related().get(email=email)

            if check_password(password, user.password):
                
                permissions = available_perm_status(user)
                
                audit.registrar_acao(
                    table='audit_user',
                    id_user=user.id,
                    response_status=status.HTTP_200_OK,
                    response_data=json.dumps({'email': email}),
                    action="Login",
                    local_code="core.views.user_auth",
                    ip_user=ip_usuario
                )

                return Response(data={'is_authenticate': True, 
                                      'is_active': user.is_active,
                                      'is_superuser': user.is_superuser,
                                      'user_id': user.id,
                                      'username': user.username,
                                      'permissions': permissions
                                      }, status=status.HTTP_200_OK)
            else:

                audit.registrar_acao(
                    table='audit_user',
                    id_user=0,
                    response_status=status.HTTP_401_UNAUTHORIZED,
                    response_data=json.dumps({"email": email}),
                    action="Login",
                    local_code="core.views.user_auth",
                    ip_user=ip_usuario
                )

                return Response(data={'is_authenticate': False}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:

            audit.registrar_acao(
                table='audit_user',
                id_user=0,
                response_status=status.HTTP_401_UNAUTHORIZED,
                response_data=json.dumps({"email": email}),
                action="Login",
                local_code="core.views.user_auth",
                ip_user=ip_usuario
            )

            return Response(data={'is_authenticate': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], url_path='register')
    def register_user(self, request):
        '''
            Registra o usuário no padrão Django concedendo permissões default
            
            Modelo de requisição POST
            ```json
            {
                "username": string,
                "email": string,
                "password": string,
                "is_active": boolean,
                "orgao": number
            }
        '''
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        is_active = request.data.get('is_active')
        orgao = request.data.get('orgao')
        
        try:
            User.objects.get(email=email)

            return Response(
                data={'error': 'Este usuário já existe'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except User.DoesNotExist:
            
            user = User.objects.create_user(username=username, email=email, password=password, is_active=is_active, is_superuser=0)
            
            orgao_include_user = AuthUserOrgao(
                id_user=user.id,
                id_orgao=orgao
            )
            orgao_include_user.save()
            
            assign_role(user, AppsAdminRoles)
            assign_role(user, PermissionsAdminRoles)
            
            return Response(
                data={'user_id': user.id, 'username': user.username, 'email': user.email},
                status=status.HTTP_201_CREATED
            )
        
    @action(detail=False, methods=['get'], url_path='list_permissions')
    def list_permissions(self,request):
        '''
            Obtem as permissões do usuario pelo id
            
            Passe na url o parametro 'user_id', exemplo:
            ```link
            /api/Auth/list_permissions/?user_id=2
        '''
        try:
            user_id = request.GET.get('user_id', None)
            
            user = User.objects.get(id=user_id)
            permissions = available_perm_status(user)
            
            return Response(
                    data=permissions,
                    status=status.HTTP_201_CREATED
                )
            
        except User.DoesNotExist:
            return Response(
                data="Usuário inexistente",
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as err:
            return Response(data={'erro': err}, status=status.HTTP_401_UNAUTHORIZED)
        
    
    @action(detail=False, methods=['post'], url_path='edit_permissions')    
    def edit_permissions(self, request):
        '''
            Edita as permissões do usuário Django
            
            Modelo de requisição POST
            ```json
            {
                'user_id': number,
                'permissions': {
                    "aalow_permission_name": True,
                    "allow_permission_name": False,
                }
            }
        '''
        try:

            user_id = request.data['user_id']
            permissions = request.data['permissions']
            user = User.objects.get(id=user_id)
            
            for role, is_perm in permissions.items():
                
                if is_perm:
                    print(f"colocando permissao {role} para o usuario {user.username}")
                    grant_permission(user, role)
                else:
                    print(f"retirando permissao {role} para o usuario {user.username}")
                    revoke_permission(user, role)
            
            return Response(data={"is_edit": True}, status=status.HTTP_200_OK)
        
        except Exception as err:
            print("erro...: ", err)
            return Response(data={"is_edit": False}, status=status.HTTP_400_BAD_REQUEST)
        