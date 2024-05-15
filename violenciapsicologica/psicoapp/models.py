from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMessage
class LocalFormulario(models.Model):

    definicaoLocalForm = models.CharField(
        max_length=255,
        default = ''
    )

    class Meta:
        verbose_name = 'Local de formulário de um usuário'
        verbose_name_plural = 'Locais de formulário de um usuário'

    def __str__(self):
        return self.definicaoLocalForm

class TipoUsuario(models.Model):

    definicaoTipo = models.CharField(
        max_length=255,
        default = ''
    )

    class Meta:
        verbose_name = 'Tipo de um usuário'
        verbose_name_plural = 'Tipos de um usuário'

    def __str__(self):
        return self.definicaoTipo


class AreaUsuario(models.Model):
    definicaoArea = models.CharField(
        max_length=255,
        default = ''
    )

    class Meta:
        verbose_name = 'Área de um usuário'
        verbose_name_plural = 'Áreas de um usuário'

    def __str__(self):
        return self.definicaoArea

class GrauInstrucao(models.Model):
    definicaoGrau = models.CharField(
        max_length=255,
        default = ''
    )

    class Meta:
        verbose_name = 'Grau de instrução'
        verbose_name_plural = 'Graus de instrução'

    def __str__(self):
        return self.definicaoGrau

# Definindo models para usuário

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Você não inseriu um endereço de e-mail inválido")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    tipo = models.ForeignKey(TipoUsuario, on_delete = models.SET_NULL, blank=True, null=True)
    area = models.ForeignKey(AreaUsuario, on_delete = models.SET_NULL, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split('@')[0]

    def get_area(self):
        return self.area.definicaoArea if self.area else None

    def get_tipo(self):
        return self.tipo.definicaoTipo if self.tipo else None

    def display_adm(self):
        return self.is_superuser

    def get_Admin(self):
        # Define o usuário como superusuário e funcionário (staff)
        self.is_superuser = True
        self.is_staff = True
        # Salva as mudanças no banco de dados
        self.save()

    def turn_Admin_off(self):
        # Remove o usuário como superusuário e funcionário (staff)
        self.is_superuser = False
        self.is_staff = False
        # Salva as mudanças no banco de dados
        self.save()

# Definindo models da aplicação

class Formulario(models.Model):
    campo_questoes = models.TextField()
    idade = models.IntegerField(
        default = 0
    )
    data_e_hora = models.DateTimeField(
        default = ''
    )
    escolha_sexo = models.CharField(
        max_length=255,
        default = ''
    )
    usuario = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)
    localAplicacao = models.ForeignKey(LocalFormulario, on_delete = models.CASCADE, blank=True, null=True)
    grauInstrucao = models.ForeignKey(GrauInstrucao, on_delete = models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Formulário'
        verbose_name_plural = 'Formulários'

    def obter_array(self):
        # Converte a string de volta para uma lista
        return list(map(str, self.campo_questoes.split(',')))

    def __str__(self):
        formatted_datetime = self.data_e_hora.strftime("%Y-%m-%d %H:%M:%S")
        return f'Formulario de {formatted_datetime}'

    def sinalizacao(self):
        formulario = self.obter_array()
        formlario_int = [eval(i) for i in formulario]

        soma = sum(formlario_int)

        if soma >= 39 and soma <= 60:
            return "Vermelho"
        else:
            if soma >= 31 and soma <= 38:
                return "Amarelo"
            else:
                if soma >= 15 and soma <= 30:
                    return "Verde"

    def sinalizacao_quantidade(self):
        formulario = self.obter_array()
        formlario_int = [eval(i) for i in formulario]

        soma = sum(formlario_int)
        return soma

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    # the below like concatinates your websites reset password url and the reset email token which will be required at a later stage
    email_plaintext_message = "Abra o link para resetar a senha" + " " + "{}{}".format(instance.request.build_absolute_uri("https://kurtmendoncaquestionario.com/recuperar-senha/"), reset_password_token.key)

    """
        this below line is the django default sending email function,
        takes up some parameter (title(email title), message(email body), from(email sender), to(recipient(s))
    """
    send_mail(
        # title:
        "Recuperação de senha do sistema {title}".format(title="Questionário Kurt Mendonça"),
        # message:
        email_plaintext_message,
        # de:
        "violenciapsi11@gmail.com",
        # to:
        [reset_password_token.user.email],
        fail_silently=False,
    )
