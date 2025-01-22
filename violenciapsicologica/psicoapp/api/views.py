from django.db.models import Count
from django.db.models.functions import TruncMonth

from urllib.parse import unquote

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import filters
from rest_framework.reverse import reverse
from rest_framework.exceptions import ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from ..models import Formulario, User, TipoUsuario, AreaUsuario, LocalFormulario, GrauInstrucao
from .serializers import FormularioSerializer, UserSerializer, TipoUsuarioSerializer, AreaUsuarioSerializer, LocalFormularioSerializer, UserPatchSerializer, GrauInstrucaoSerializer, FormularioDispersaoSerializer, FormularioDesvioPadraoSerializer, UserAdminSerializer

import locale
from datetime import datetime, timedelta
from django.utils import timezone
from calendar import monthrange

from ..views import get_dispersao, get_desvio, get_pizza, get_bar

# Raiz da Api

class APIRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'tipos': reverse('psicoapp:tipo_list', request=request, format=format),
            'usuários': reverse('psicoapp:user_list', request=request, format=format),
            'registro de usuário': reverse('psicoapp:user_registration', request=request, format=format),
            'formulários': reverse('psicoapp:formulario_todos', request=request, format=format),
            'filtro de formulários': reverse('psicoapp:formulario_filtrado', request=request, format=format),
            'formulários de todos meses': reverse('psicoapp:formulario_mes', request=request, format=format),
            # 'formulários por mês': reverse('psicoapp:formulario_mes_escolhido', kwargs={'pk': 1}, request=request, format=format),
            'quantidade de formulários': reverse('psicoapp:formulario_quantidade', request=request, format=format),
            'novo formulário': reverse('psicoapp:formulario_novo', request=request, format=format),
            'quantidade de respostas': reverse('psicoapp:formulario_respostas', request=request, format=format),
            'sinalização': reverse('psicoapp:formulario_sinalizacao', request=request, format=format),
            'token auth': reverse('psicoapp:token_obtain_pair', request=request, format=format),
            'token refresh': reverse('psicoapp:token_refresh', request=request, format=format),
        })

# Filtro de formulários
class DesvioPadraoFiltro(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        idade = request.query_params.get('idade')
        sexo = request.query_params.get('sexo')
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        grau_instrucao = request.query_params.get('grau_instrucao')
        local_aplicacao = request.query_params.get('local_aplicacao')
        usuario = request.query_params.get('usuario')
        area = request.query_params.get('area')
        tipo_usuario = request.query_params.get('tipo_usuario')
        idade_min = request.query_params.get('idade_min')
        idade_max = request.query_params.get('idade_max')
        encaminhado_por = request.query_params.get('encaminhado_por')
        especialidade = request.query_params.get('especialidade')
        prontuario = request.query_params.get('prontuario')

        if data_inicio and data_fim:
            try:
                # Decodifique os valores dos parâmetros de data
                data_inicio_decodificada = unquote(data_inicio)
                data_fim_decodificada = unquote(data_fim)

                # Converta as strings para objetos datetime
                data_inicio_objeto = datetime.strptime(data_inicio_decodificada, '%Y-%m-%d %H:%M')
                data_fim_objeto = datetime.strptime(data_fim_decodificada, '%Y-%m-%d %H:%M')

            except ValueError:
                raise ParseError(detail='Formato de data de início inválido. Use o formato YYYY-MM-DD HH:MM.')

            if data_inicio_objeto > data_fim_objeto:
                raise Exception("A data de início deve ser menor que a data de fim da busca")

            # Use os objetos datetime na filtragem do queryset
            queryset = queryset.filter(data_e_hora__gte=data_inicio_objeto, data_e_hora__lte=data_fim_objeto)

        if usuario:
            queryset = queryset.filter(usuario__name=usuario)
        else:
            if tipo_usuario:
                queryset = queryset.filter(usuario__tipo__definicaoTipo=tipo_usuario)
            if area:
                queryset = queryset.filter(usuario__area__definicaoArea=area)

        if idade_min and idade_max:
            try:
                queryset = queryset.filter(idade__gte=idade_min, idade__lte=idade_max)
                print(queryset)
            except:
                raise Exception("Houve um erro na definição de idades")
        else:
            if idade:
                queryset = queryset.filter(idade=idade)

        if sexo:
            queryset = queryset.filter(escolha_sexo=sexo)

        if grau_instrucao:
            grau_filter = GrauInstrucao.objects.get(definicaoGrau=grau_instrucao)
            queryset = queryset.filter(grauInstrucao=grau_filter)

        if local_aplicacao:
            local_app = LocalFormulario.objects.get(definicaoLocalForm=local_aplicacao)
            queryset = queryset.filter(localAplicacao=local_app)

        if encaminhado_por:
            queryset = queryset.filter(encaminhado_por=encaminhado_por)

        if especialidade:
            queryset = queryset.filter(especialidade=especialidade)

        if prontuario:
            queryset = queryset.filter(prontuario=prontuario)


        return queryset


class FormularioFiltro(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        idade = request.query_params.get('idade')
        sexo = request.query_params.get('sexo')
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        grau_instrucao = request.query_params.get('grau_instrucao')
        local_aplicacao = request.query_params.get('local_aplicacao')
        usuario = request.query_params.get('usuario')
        area = request.query_params.get('area')
        tipo_usuario = request.query_params.get('tipo_usuario')
        idade_min = request.query_params.get('idade_min')
        idade_max = request.query_params.get('idade_max')

        if data_inicio and data_fim:
            try:
                # Decodifique os valores dos parâmetros de data
                data_inicio_decodificada = unquote(data_inicio)
                data_fim_decodificada = unquote(data_fim)

                # Converta as strings para objetos datetime
                data_inicio_objeto = datetime.strptime(data_inicio_decodificada, '%Y-%m-%d %H:%M')
                data_fim_objeto = datetime.strptime(data_fim_decodificada, '%Y-%m-%d %H:%M')

            except ValueError:
                raise ParseError(detail='Formato de data de início inválido. Use o formato YYYY-MM-DD HH:MM.')

            if data_inicio_objeto > data_fim_objeto:
                raise Exception("A data de início deve ser menor que a data de fim da busca")

            # Use os objetos datetime na filtragem do queryset
            queryset = queryset.filter(data_e_hora__gte=data_inicio_objeto, data_e_hora__lte=data_fim_objeto)

        if usuario:
            queryset = queryset.filter(usuario__name=usuario)
        else:
            if tipo_usuario:
                queryset = queryset.filter(usuario__tipo__definicaoTipo=tipo_usuario)
            if area:
                queryset = queryset.filter(usuario__area__definicaoArea=area)

        if idade_min and idade_max:
            try:
                queryset = queryset.filter(idade__gte=idade_min, idade__lte=idade_max)
            except:
                raise Exception("Houve um erro na definição de idades")
        else:
            if idade:
                queryset = queryset.filter(idade=idade)

        if sexo:
            queryset = queryset.filter(escolha_sexo=sexo)

        if grau_instrucao:
            grau_filter = GrauInstrucao.objects.get(definicaoGrau=grau_instrucao)
            queryset = queryset.filter(grauInstrucao=grau_filter)

        if local_aplicacao:
            local_app = LocalFormulario.objects.get(definicaoLocalForm=local_aplicacao)
            queryset = queryset.filter(localAplicacao=local_app)

        return queryset

# Definição de endpoints de autenticação

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.get_full_name()
        token['tipo'] = user.get_area()
        token['area'] = user.get_tipo()
        token['is_superuser'] = user.is_superuser

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout realizado com sucesso."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Falha ao processar a solicitação de logout."}, status=status.HTTP_400_BAD_REQUEST)


# Definição de endpoints
class CriaFormulario(generics.CreateAPIView):
    serializer_class = FormularioSerializer

    def perform_create(self, serializer):
        # Adicione a data e hora antes de salvar o objeto
        serializer.save(
            data_e_hora=(datetime.now() - timedelta(hours=3)),
            usuario=self.request.user)


class FormularioIdView(generics.RetrieveUpdateAPIView):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer
    lookup_field = 'id'



class TotalFormulariosView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, *args, **kwargs):
        total_formularios = Formulario.objects.count()
        return Response({"total_formularios": total_formularios}, status=status.HTTP_200_OK)


class ExibirTodosFormularios(generics.ListAPIView):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer
    filter_backends = [FormularioFiltro]


class FormulariosPorMes(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, *args, **kwargs):
        # Configura o locale para português (Brasil)
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

        # Filtra os formulários criados no último ano (altere conforme necessário)
        formularios_por_mes = Formulario.objects.filter(
            data_e_hora__gte=datetime.now().replace(year=datetime.now().year - 1)
        ).annotate(
            mes=TruncMonth('data_e_hora')
        ).values('mes').annotate(total=Count('id')).order_by('mes')

        # Crie um dicionário com os resultados
        resultados = {mes['mes'].strftime('%b').capitalize(): mes['total'] for mes in formularios_por_mes}

        # Restaura o locale padrão
        locale.setlocale(locale.LC_TIME, '')

        return Response(resultados, status=200)


class FormularioPorMesEscolhido(APIView):
    """
    Retorna a contagem de formulários em período de dias de cada mês escolhido. É necessário inserir o valor de um mês no campo id.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, pk, *args, **kwargs):
        mes = pk
        ano_atual = timezone.now().year


        # Configura o locale para português (Brasil)
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

        # Dia 01 até 05
        primeiro_dia_1 = timezone.datetime(ano_atual, mes, 1, 0, 0)
        ultimo_dia_1 = timezone.datetime(ano_atual, mes, 5, 23, 59)

        form_1 = Formulario.objects.filter(
            data_e_hora__gte=primeiro_dia_1,
            data_e_hora__lte=ultimo_dia_1
        )

        # Dia 06 até 10
        primeiro_dia_2 = timezone.datetime(ano_atual, mes, 6, 0, 0, 0)
        ultimo_dia_2 = timezone.datetime(ano_atual, mes, 10, 23, 59, 59)

        form_2 = Formulario.objects.filter(
            data_e_hora__gte=primeiro_dia_2,
            data_e_hora__lte=ultimo_dia_2
        )

        # Dia 11 até 15
        primeiro_dia_3 = timezone.datetime(ano_atual, mes, 11, 0, 0, 0)
        ultimo_dia_3 = timezone.datetime(ano_atual, mes, 15, 23, 59, 59)

        form_3 = Formulario.objects.filter(
            data_e_hora__gte=primeiro_dia_3,
            data_e_hora__lte=ultimo_dia_3
        )

        # Dia 16 até 20
        primeiro_dia_4 = timezone.datetime(ano_atual, mes, 16, 0, 0, 0)
        ultimo_dia_4 = timezone.datetime(ano_atual, mes, 20, 23, 59, 59)

        form_4 = Formulario.objects.filter(
            data_e_hora__gte=primeiro_dia_4,
            data_e_hora__lte=ultimo_dia_4
        )

        # Dia 21 até 25
        primeiro_dia_5 = timezone.datetime(ano_atual, mes, 21, 0, 0, 0)
        ultimo_dia_5 = timezone.datetime(ano_atual, mes, 25, 23, 59, 59)

        form_5 = Formulario.objects.filter(
            data_e_hora__gte=primeiro_dia_5,
            data_e_hora__lte=ultimo_dia_5
        )

        # Dias restantes
        ultimo_dia_mes = monthrange(ano_atual, mes)[1]
        primeiro_dia_6 = timezone.datetime(ano_atual, mes, 26, 0, 0, 0)
        ultimo_dia_6 = timezone.datetime(ano_atual, mes, ultimo_dia_mes, 23, 59, 59)

        form_6 = Formulario.objects.filter(
            data_e_hora__gte=primeiro_dia_6,
            data_e_hora__lte=ultimo_dia_6
        )
        dicionario = {
            f"01/{mes} até 05/{mes}": form_1.aggregate(total=Count('id'))['total'],
            f"06/{mes} até 10/{mes}": form_2.aggregate(total=Count('id'))['total'],
            f"11/{mes} até 15/{mes}": form_3.aggregate(total=Count('id'))['total'],
            f"16/{mes} até 20/{mes}": form_4.aggregate(total=Count('id'))['total'],
            f"21/{mes} até 25/{mes}": form_5.aggregate(total=Count('id'))['total'],
            f"26/{mes} até {ultimo_dia_6.day}/{mes}": form_6.aggregate(total=Count('id'))['total'],
        }

        return Response(dicionario, status=200)


class FormularioFiltrado(generics.ListAPIView):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer
    permission_classes = (IsAdminUser,)

    filter_backends = [FormularioFiltro]


class DispersaoFormulario(generics.ListAPIView):
    queryset = Formulario.objects.all()
    serializer_class = FormularioDispersaoSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [FormularioFiltro]

# Desvio Padrão
class DesvioPadraoFormulario(generics.ListAPIView):
    queryset = Formulario.objects.all()
    serializer_class = FormularioDesvioPadraoSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [DesvioPadraoFiltro]

# Sinalização
class SinaisFormularios(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        queryset = Formulario.objects.all()
        filtro = FormularioFiltro()

        # Aplica o filtro
        queryset = filtro.filter_queryset(request, queryset, self)

        verde = 0
        amarelo = 0
        vermelho = 0

        for formulario in queryset:
            sinal = formulario.sinalizacao()
            if sinal == "Vermelho":
                vermelho += 1
            elif sinal == "Amarelo":
                amarelo += 1
            elif sinal == "Verde":
                verde += 1

        sinais = {"Vermelho": vermelho, "Amarelo": amarelo, "Verde": verde}

        return Response(sinais, status=200)

# Quantidade de perguntas
class QuantidadeRespostas(APIView):
    """
    Retorna a contagem de respostas para cada categoria do gráfico de respostas por opção.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        queryset = Formulario.objects.all()
        filtro = FormularioFiltro()

        # Aplica o filtro
        queryset = filtro.filter_queryset(request, queryset, self)
        total_formularios = queryset
        nunca = 0
        as_vezes = 0
        frequentemente = 0
        sempre = 0

        for formulario in total_formularios:
            questoes = formulario.obter_array()
            for questao in questoes:
                if questao == "1":
                    nunca+=1
                else:
                    if questao == "2":
                        as_vezes +=1
                    else:
                        if questao == "3":
                            frequentemente+=1
                        else:
                            sempre +=1
        resultado = {"Nunca" : nunca, "As vezes": as_vezes, "Frequentemente": frequentemente, "Sempre": sempre}

        return Response(resultado, status=200)

# Gerenciamento de usuários
class UserRegistrationAPIView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAdminRegistrationAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = UserAdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Obtém o usuário salvo
            user.get_Admin()  # Chama o método get_Admin para tornar o usuário um administrador
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Usuario(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UsuarioId(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserPatchSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        # Recupere o ID do usuário
        user_id = self.kwargs['id']

        # Obtenha o usuário com base no ID
        user = User.objects.get(id=user_id)
        parametro = self.request.query_params.get('parametro')
        if parametro == 'on':
            # Acione o método get_Admin
            user.get_Admin()
        elif parametro == 'off':
            # Acione o método turn_Admin_off
            user.turn_Admin_off()

        # Continue com a lógica de atualização padrão
        return super().update(request, *args, **kwargs)

# Tipo de usuário
class CreateTipoUsuarioView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)

    serializer_class = TipoUsuarioSerializer


class TipoUsuarioView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer


class TipoUsuarioIdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer
    lookup_field = 'id'

# Área de usuario
class CreateAreaUsuarioView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)

    serializer_class = AreaUsuarioSerializer


class AreaUsuarioView(generics.ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = AreaUsuario.objects.all()
    serializer_class = AreaUsuarioSerializer


class AreaUsuarioIdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = AreaUsuario.objects.all()
    serializer_class = AreaUsuarioSerializer
    lookup_field = 'id'


# Local
class CreateLocalAplicacaoView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = LocalFormularioSerializer


class LocalAplicacaoView(generics.ListAPIView):
    queryset = LocalFormulario.objects.all()
    serializer_class = LocalFormularioSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

class LocalAplicacaoIdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = LocalFormulario.objects.all()
    serializer_class = LocalFormularioSerializer
    lookup_field = 'id'


# Grau
class CreateGrauInstrucaoView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = GrauInstrucaoSerializer


class GrauInstrucaoView(generics.ListAPIView):
    queryset = GrauInstrucao.objects.all()
    serializer_class = GrauInstrucaoSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]


class GrauInstrucaoIdView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser, IsAuthenticated,)
    queryset = GrauInstrucao.objects.all()
    serializer_class = GrauInstrucaoSerializer
    lookup_field = 'id'

# imagens pro pdf
class DocPDF(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            queryset = Formulario.objects.all()
            filtro = FormularioFiltro()

            # Aplica o filtro
            queryset = filtro.filter_queryset(request, queryset, self)
            resultado = {}

            dispersao = get_dispersao(queryset)
            desvio = get_desvio(queryset)
            bar = get_bar(queryset)
            pizza = get_pizza(queryset)

            resultado['Dispersao'] = dispersao
            resultado['Desvio'] = desvio
            resultado['Barra'] = bar
            resultado['Pizza'] = pizza

            return Response(resultado, status=200)
        except Exception as e:
            resultado = {"Erro": e}

            return Response(resultado, status=500)

