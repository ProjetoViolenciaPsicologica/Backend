from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import CriaFormulario, TotalFormulariosView, ExibirTodosFormularios, FormulariosPorMes, MyTokenObtainPairView, SinaisFormularios, QuantidadeRespostas, FormularioPorMesEscolhido, FormularioFiltrado, APIRoot, UserRegistrationAPIView, Usuario, UsuarioId, TipoUsuarioView, TipoUsuarioIdView, AreaUsuarioView, AreaUsuarioIdView, LocalAplicacaoView, LocalAplicacaoIdView, GrauInstrucaoIdView, GrauInstrucaoView, DispersaoFormulario, DesvioPadraoFormulario, LogoutView, UserAdminRegistrationAPIView, CreateGrauInstrucaoView, CreateLocalAplicacaoView, CreateAreaUsuarioView, CreateTipoUsuarioView, DocPDF, FormularioIdView
from django.urls import include

app_name = 'psicoapp'

urlpatterns = [
    path('', APIRoot.as_view(), name='api_root'),
    path('graficosPDF', DocPDF.as_view(), name='graficosPDF'),
    path('dispersao', DispersaoFormulario.as_view(), name='dispersao_list'),
    path('desvio', DesvioPadraoFormulario.as_view(), name='desvio_list'),
    path('area', AreaUsuarioView.as_view(), name='area_list'),
    path('area/create', CreateAreaUsuarioView.as_view(), name='area_create'),
    path('area/<int:id>', AreaUsuarioIdView.as_view(), name='area_list'),
    path('grau', GrauInstrucaoView.as_view(), name='grau_list'),
    path('grau/create', CreateGrauInstrucaoView.as_view(), name='grau_create'),
    path('grau/<int:id>', GrauInstrucaoIdView.as_view(), name='grau_list'),
    path('tipo', TipoUsuarioView.as_view(), name='tipo_list'),
    path('tipo/create', CreateTipoUsuarioView.as_view(), name='tipo_create'),
    path('tipo/<int:id>', TipoUsuarioIdView.as_view(), name='tipo_manager'),
    path('local', LocalAplicacaoView.as_view(), name='local_list'),
    path('local/create', CreateLocalAplicacaoView.as_view(), name='local_create'),
    path('local/<int:id>', LocalAplicacaoIdView.as_view(), name='local_manager'),
    path('user', Usuario.as_view(), name='user_list'),
    path('user/<int:id>', UsuarioId.as_view(), name='user_manager'),
    path('user/register', UserRegistrationAPIView.as_view(), name='user_registration'),
    path('user/admin/register', UserAdminRegistrationAPIView.as_view(), name='user_admin_registration'),
    path('formulario/novo', CriaFormulario.as_view(), name='formulario_novo'),
    path('formulario/quantidade', TotalFormulariosView.as_view(), name='formulario_quantidade'),
    path('formulario', ExibirTodosFormularios.as_view(), name='formulario_todos'),
    path('formulario/<int:id>', FormularioIdView.as_view(), name='formulario_manager'),
    path('formulario/filtro/', FormularioFiltrado.as_view(), name='formulario_filtrado'),
    path('formulario/porMes', FormulariosPorMes.as_view(), name='formulario_mes'),
    path('formulario/porMes/<int:pk>', FormularioPorMesEscolhido.as_view(), name='formulario_mes_escolhido'),
    path('formulario/sinalizacao', SinaisFormularios.as_view(), name='formulario_sinalizacao'),
    path('formulario/quantidadeRespostas', QuantidadeRespostas.as_view(), name='formulario_respostas'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('logout/', LogoutView.as_view(), name='auth_logout'),

    # sistema de autenticação
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]