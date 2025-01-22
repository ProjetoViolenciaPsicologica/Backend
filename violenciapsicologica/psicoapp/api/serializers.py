from rest_framework import serializers
from ..models import Formulario, User, TipoUsuario, AreaUsuario, LocalFormulario, GrauInstrucao

class TipoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUsuario
        fields = ('id', 'definicaoTipo')

class AreaUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaUsuario
        fields = ('id', 'definicaoArea')

class LocalFormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalFormulario
        fields = ('id', 'definicaoLocalForm')

class GrauInstrucaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrauInstrucao
        fields = ('id', 'definicaoGrau')

class UserAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password')

        extra_kwargs = {
            'password': {'write_only': True},
            'name': {'help_text': 'Exemplo: exemplo_usuario'},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['admstatus'] = instance.display_adm()
        return representation

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    tipo = TipoUsuarioSerializer()
    area = AreaUsuarioSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password', 'tipo', 'area')

        extra_kwargs = {
            'password': {'write_only': True},
            'name': {'help_text': 'Exemplo: exemplo_usuario'},
            }

    def create(self, validated_data):
        tipo_data = validated_data.pop('tipo')
        area_data = validated_data.pop('area')
        tipo_instance = TipoUsuario.objects.get_or_create(**tipo_data)[0]
        area_instance = AreaUsuario.objects.get_or_create(**area_data)[0]
        user = User.objects.create_user(tipo=tipo_instance, area=area_instance, **validated_data)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['admstatus'] = instance.display_adm()
        return representation


class UserPatchSerializer(serializers.ModelSerializer):
    tipo = TipoUsuarioSerializer()
    area = AreaUsuarioSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'tipo', 'area')

    def create(self, validated_data):
        tipo_data = validated_data.pop('tipo')
        area_data = validated_data.pop('area')
        tipo_instance = TipoUsuario.objects.get_or_create(**tipo_data)[0]
        area_instance = AreaUsuario.objects.get_or_create(**area_data)[0]
        user = User.objects.create_user(tipo=tipo_instance, area=area_instance, **validated_data)
        return user

    def update(self, instance, validated_data):
        tipo_data = validated_data.pop('tipo', {})  # Handle the possibility of tipo not being in validated_data
        area_data = validated_data.pop('area', {})  # Handle the possibility of area not being in validated_data

        # Update nested serializer data (tipo and area)
        tipo_instance, _ = TipoUsuario.objects.get_or_create(**tipo_data)
        area_instance, _ = AreaUsuario.objects.get_or_create(**area_data)

        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.tipo = tipo_instance
        instance.area = area_instance

        instance.save()
        return instance



class FormularioSerializer(serializers.ModelSerializer):
    localAplicacao = LocalFormularioSerializer()
    grauInstrucao = GrauInstrucaoSerializer()

    class Meta:
        model = Formulario
        fields = ("id", "campo_questoes", "idade", "escolha_sexo", "localAplicacao", 'grauInstrucao', 'encaminhado_por', 'especialidade', 'prontuario')

    def create(self, validated_data):
        local_data = validated_data.pop('localAplicacao')
        local_instance = LocalFormulario.objects.get_or_create(**local_data)[0]
        grau_data = validated_data.pop('grauInstrucao')
        grau_instance = GrauInstrucao.objects.get_or_create(**grau_data)[0]
        formulario = Formulario.objects.create(localAplicacao=local_instance, grauInstrucao=grau_instance, **validated_data)
        return formulario


class FormularioDispersaoSerializer(serializers.ModelSerializer):
    grauInstrucao = GrauInstrucaoSerializer()
    class Meta:
        model = Formulario
        fields = ("id", 'grauInstrucao', 'campo_questoes', 'idade')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sinalizacao'] = instance.sinalizacao()
        return representation


class FormularioDesvioPadraoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulario
        fields = ("id", 'data_e_hora', 'campo_questoes')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sinalizacao'] = instance.sinalizacao()
        return representation

