from rolepermissions.roles import AbstractUserRole

class ApiRoles(AbstractUserRole):
    available_permissions = {
        'allow_canal_avaliacao': False,
        'allow_canal_prestacao': False,
        'allow_opcoes': False,
        'allow_orgao': False,
        'allow_perguntas': False,
        'allow_pesquisas': False,
        'allow_questionarios': False,
        'allow_respostas': False,
        'allow_servico': False,
        'allow_tipo_pergunta': False,
        'allow_tipo_servico': False,
        'allow_user_auth': False,
        'allow_user_group': False,
        'allow_webhook': False,
        'allow_dashboard': False,
    }  
    
class PermissionsAdminRoles(AbstractUserRole):
    available_permissions = {
        'allow_admin_dashboard': False,
        'allow_admin_questionarios': False,
        'allow_admin_avaliacao': False,
        'allow_admin_respostas': False,
        'allow_admin_usuarios': False,
        'allow_admin_canais': False,
        'allow_admin_configuracoes': False,

    }
    
class AppsAdminRoles(AbstractUserRole):
    available_permissions = {
        'allow_app_dashboards_nps': False,
        'allow_app_questionario_criar_questionario': False,
        'allow_app_questionario_listagem_questionario': False,
        'allow_app_avaliacao_gerar_avaliacao': False,
        'allow_app_resposta_listagem': False,
        'allow_app_usuario_gerencia_usuario': False,
        'allow_app_canais_listagem': False,
        'allow_app_configuracoes_orgao': False,
        'allow_app_configuracoes_servicos': False,
        'allow_app_confguracoes_tipos_servicos': False,
        'allow_app_configuracoes_webhhok': False,
    }