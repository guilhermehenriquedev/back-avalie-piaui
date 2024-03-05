from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    homeviews,
    avaliacao,
    canal_avaliacao,
    pesquisas,
    orgao,
    perguntas,
    tipo_pergunta,
    opcoes,
    respostas,
    canal_prestacao,
    servico,
    tipo_servico,
    user_auth,
    questionario,
    webhook,
    check_token,
    dashboard,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()

router.register(r'Avaliacao', avaliacao.AvaliacaoViewSet, basename='Avaliacao')
router.register(r'CanalAvaliacao', canal_avaliacao.CanalAvaliacaoViewSet, basename='CanalAvaliacao')
router.register(r'Pesquisas', pesquisas.PesquisasViewSet, basename='Pesquisas')
router.register(r'Orgao', orgao.OrgaoViewSet, basename='Orgao')
router.register(r'Perguntas', perguntas.PerguntasViewSet, basename='Perguntas')
router.register(r'TipoPergunta', tipo_pergunta.TipoPerguntaViewSet, basename='TipoPergunta')
router.register(r'Opcoes', opcoes.OpcoesViewSet, basename='Opcoes')
router.register(r'Respostas', respostas.RespostasViewSet, basename='Respostas')
router.register(r'CanalPrestacao', canal_prestacao.CanalPrestacaoViewSet, basename='CanalPrestacao')
router.register(r'Servico', servico.ServicoViewSet, basename='Servico')
router.register(r'TipoServico', tipo_servico.TipoServiceViewSet, basename='TipoServico')
router.register(r'Auth', user_auth.UserAuthViewSet, basename='Auth')
router.register(r'Questionario', questionario.QuestionarioViewSet, basename='Questionario')
router.register(r'Webhook', webhook.WebhookViewSet, basename='Webhook')
router.register(r'Verify', check_token.TokenValidationViewSet, basename='Verify')
router.register(r'Dashboard', dashboard.Dashboard, basename='Dashboard')

schema_view = get_schema_view(
    openapi.Info(
        title="API Avalie PI",
        default_version='v2.3',
        description="Aplicação de sistema de avaliação dos orgãos e serviços do Estado do Piauí",
        contact=openapi.Contact(email="guilherme.fernandes@sead.pi.gov.br"),
        license=openapi.License(name="SEAD"),
    ),
    public=True,
)

urlpatterns = [
    path('', homeviews.index, name="index"),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
