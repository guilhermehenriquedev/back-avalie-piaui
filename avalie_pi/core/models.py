from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User

class Avaliacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    hash = models.CharField(max_length=100, null=True)
    idService = models.IntegerField(null=True)
    idOrgao = models.IntegerField(null=True)
    cpf = models.BigIntegerField(null=True)
    protocolo = models.CharField(max_length=100, null=True)
    idCanalPrestacao = models.IntegerField(null=True)
    idCanalAvaliacao = models.IntegerField(null=True)
    idPesquisa = models.IntegerField(null=True)
    criado_em = models.DateTimeField(null=True)
    respondido_em = models.DateTimeField(null=True)
    nome = models.TextField(default='sem_nome')
    telefone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'Avaliacao'

class CanalAvaliacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=True)
    ativo = models.BooleanField(null=True)

    class Meta:
        db_table = 'Canal_avalicao'

class CanalPrestacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=True)
    ativo = models.BooleanField(null=True)

    class Meta:
        db_table = 'Canal_prestacao'

class Orgao(models.Model):
    id = models.AutoField(primary_key=True)
    idSEI = models.IntegerField(null=True)
    nome = models.CharField(max_length=255, null=True)
    nome_curto = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255, null=True)
    descricao = models.CharField(max_length=255, null=True)
    ativo = models.BooleanField(null=True)

    class Meta:
        db_table = 'Orgao'

class Respostas(models.Model):
    response_id = models.AutoField(primary_key=True)
    cpf = models.BigIntegerField(null=True)
    id_avaliacao = models.CharField(max_length=100, null=True)
    survey_id = models.IntegerField(null=True)
    question_id = models.IntegerField(null=True)
    option_id = models.IntegerField(null=True)
    texto_resposta = models.TextField()
    criado_em = models.DateTimeField(null=True)
    atualizado_em = models.DateTimeField(null=True)

    class Meta:
        db_table = 'Respostas'

class Servico(models.Model):
    id = models.AutoField(primary_key=True)
    idOrgao = models.IntegerField(null=True)
    id_tipoService = models.IntegerField(null=True)
    nome = models.CharField(max_length=255, null=True)
    descricao = models.CharField(max_length=255, null=True)
    ativo = models.BooleanField(null=True)

    class Meta:
        db_table = 'Servico'

class TipoService(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=True)
    ativo = models.BooleanField(null=True)

    class Meta:
        db_table = 'TipoService'

class TipoPergunta(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=True)
    ativo = models.BooleanField(null=True)

    class Meta:
        db_table = 'Tipo_pergunta'

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    ddd = models.CharField(max_length=2, null=True)
    telefone = models.CharField(max_length=9, null=True)
    cargo = models.CharField(max_length=100, null=True)
    cpf = models.CharField(max_length=11, null=True)
    orgao_id = models.IntegerField(null=True)
    criado_em = models.DateTimeField(null=True)
    atualizado_em = models.DateTimeField(null=True)
    delete = models.BooleanField(null=True)

    class Meta:
        db_table = 'Users'

class UserAuth(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    user_group = models.IntegerField()
    cpf = models.CharField(max_length=100)
    email = models.CharField(max_length=250, null=True)

    class Meta:
        db_table = 'user_auth'

class UserGroup(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100, null=False)
    is_active = models.BooleanField(null=True)

    class Meta:
        db_table = 'user_groups'


class Pesquisas(models.Model):
    survey_id = models.AutoField(primary_key=True)
    orgao_id = models.IntegerField(null=True)
    titulo = models.CharField(max_length=100, null=True)
    descricao = models.CharField(max_length=255, null=True)
    criado_em = models.DateTimeField(null=True)
    atualizado_em = models.DateTimeField(null=True)
    user_id = models.IntegerField(null=True)
    is_active = models.BooleanField(null=False)
    tipo_servico = models.IntegerField(null=False)
    estado = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'Pesquisas'

class Perguntas(models.Model):
    id = models.AutoField(primary_key=True)
    texto_pergunta = models.TextField(null=True)
    tipo_pergunta = models.IntegerField(null=True)
    criado_em = models.DateTimeField(null=True)
    atualizado_em = models.DateTimeField(null=True)
    survey_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'Perguntas'

class Opcoes(models.Model):
    option_id = models.AutoField(primary_key=True)
    texto_opcao = models.TextField()
    criado_em = models.DateTimeField(null=True)
    atualizado_em = models.DateTimeField(null=True)
    pergunta_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'Opcoes'

class Webhook(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100, null=True)
    webhook = models.TextField(null=True)
    is_active = models.BooleanField(null=True)
    atualizado_em = models.DateTimeField(null=True)

    class Meta:
        db_table = 'webhook'
        

class WebhookRuntime(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)
    status_code = models.IntegerField()
    date = models.DateTimeField(null=True)
    runtime = models.TimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'webhook_runtime'
        
class AuthUserOrgao(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.IntegerField()
    id_orgao = models.IntegerField()
    
    class Meta:
        db_table = 'auth_user_orgao'
        
    def nome_orgao(self):
        try:
            orgao = Orgao.objects.get(id=self.id_orgao)
            return orgao.nome
        except Orgao.DoesNotExist:
            return None

