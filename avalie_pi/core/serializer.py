from rest_framework import serializers
from core.models import *

from django.contrib.auth.models import User

class AuthUserOrgaoSerializer(serializers.ModelSerializer):
    nome_orgao = serializers.SerializerMethodField()
    class Meta:
        model = AuthUserOrgao
        fields = ['id','id_user', 'id_orgao', 'nome_orgao']
        
    def get_nome_orgao(self, obj):
        return obj.nome_orgao()

class UserSerializer(serializers.ModelSerializer):
    orgao_name = serializers.SerializerMethodField()
    orgao_id = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'password', 'orgao_name', 'orgao_id']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'password': {'required': False}
        }

    def get_orgao_name(self, obj):
        try:
            auth_user_orgao = AuthUserOrgao.objects.get(id_user=obj.id)
            return auth_user_orgao.nome_orgao()
        except AuthUserOrgao.DoesNotExist:
            return None
        
    def get_orgao_id(self, obj):
        try:
            auth_user_orgao = AuthUserOrgao.objects.get(id_user=obj.id)
            return auth_user_orgao.id_orgao
        except AuthUserOrgao.DoesNotExist:
            return None

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'

class CanalAvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanalAvaliacao
        fields = '__all__'

class CanalPrestacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanalPrestacao
        fields = '__all__'

class OrgaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orgao
        fields = '__all__'

class RespostasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respostas
        fields = '__all__'

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'

class TipoServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoService
        fields = '__all__'
        
class TipoPerguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPergunta
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        fields = '__all__'

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'


class PerguntasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Perguntas
        fields = '__all__'

class OpcoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcoes
        fields = '__all__'

class PesquisasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pesquisas
        fields = '__all__'

class WebhookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Webhook
        fields = '__all__'
        

