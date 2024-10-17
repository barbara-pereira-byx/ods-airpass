from django.utils import timezone
import re
from django.core.exceptions import ValidationError
from .choices import CARGOS, GENEROS, CLASSES, STATUS
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator, RegexValidator
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

##----------------------------------------------- VALIDAÇÕES -----------------------------------------------------

def validar_data_reserva(value):
    """
    Valida se a data da reserva não é no passado.

    Args:
        value (datetime): A data a ser validada.

    Raises:
        ValidationError: Se a data da reserva for menor que a data e hora atuais.
    """
    if value < timezone.now():
        raise ValidationError('A data da reserva não pode ser no passado.')

def validar_cpf_passaporte(value):
    """
    Valida o formato do CPF ou do passaporte.

    O CPF deve estar no formato XXX.XXX.XXX-XX e o passaporte deve ter entre 5 e 20 caracteres,
    podendo incluir letras e números.

    Args:
        value (str): O CPF ou passaporte a ser validado.

    Raises:
        ValidationError: Se o valor não corresponder ao formato de CPF ou passaporte válido.
    """
    cpf_pattern = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
    passaporte_pattern = re.compile(r'^[A-Za-z0-9]{5,20}$')

    if not cpf_pattern.match(value) and not passaporte_pattern.match(value):
        raise ValidationError('O campo deve estar no formato de CPF (XXX.XXX.XXX-XX) ou um passaporte válido.')

def validar_email(value):
    """
    Valida o formato do e-mail.

    O e-mail deve estar em um formato válido, como exemplo@dominio.com.

    Args:
        value (str): O e-mail a ser validado.

    Raises:
        ValidationError: Se o valor não corresponder ao formato de e-mail válido.
    """
    email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    if not email_pattern.match(value):
        raise ValidationError('O e-mail deve estar em um formato válido (exemplo: nome@dominio.com).')



class FuncionarioManager(BaseUserManager):
    """
    Gerenciador de usuários para o modelo Funcionario.

    Esta classe fornece métodos para criar usuários e superusuários.
    """

    def create_user(self, email, cpf, nome, data_nascimento, password=None):
        """
        Cria e salva um novo usuário Funcionario com um email, CPF e senha.

        Args:
            email (str): O e-mail do funcionário. Deve ser fornecido.
            cpf (str): O CPF do funcionário. Deve ser fornecido.
            nome (str): O nome do funcionário. Deve ser fornecido.
            data_nascimento (datetime): A data de nascimento do funcionário.
            cargo (int): O cargo do funcionário, representado por um inteiro.
            password (str, optional): A senha do funcionário. Se não fornecida, será definida como None.

        Raises:
            ValueError: Se o e-mail, CPF ou nome não forem fornecidos.

        Returns:
            Funcionario: O novo objeto Funcionario criado e salvo no banco de dados.
        """
        if not email:
            raise ValueError('O email deve ser fornecido')
        if not cpf:
            raise ValueError('O CPF deve ser fornecido')
        if not nome:
            raise ValueError('O nome deve ser fornecido')

        email = self.normalize_email(email)
        funcionario = self.model(
            email=email,
            cpf=cpf,
            nome=nome,
            data_nascimento=data_nascimento,
        )
        funcionario.set_password(password)  # Define a senha
        funcionario.save(using=self._db)
        return funcionario

    def create_superuser(self, email, cpf, nome, data_nascimento, password=None):
        """
        Cria e salva um novo superusuário Funcionario com um e-mail, CPF e senha.

        Args:
            email (str): O e-mail do funcionário. Deve ser fornecido.
            cpf (str): O CPF do funcionário. Deve ser fornecido.
            nome (str): O nome do funcionário. Deve ser fornecido.
            data_nascimento (datetime): A data de nascimento do funcionário.
            cargo (int): O cargo do funcionário, representado por um inteiro.
            password (str, optional): A senha do funcionário. Se não fornecida, será definida como None.

        Returns:
            Funcionario: O novo objeto Funcionario criado e salvo no banco de dados, com permissões de superusuário.
        """
        funcionario = self.create_user(
            email,
            cpf,
            nome,
            data_nascimento,
            password=password,
        )
        funcionario.is_superuser = True
        funcionario.is_staff = True
        funcionario.save(using=self._db)
        return funcionario


##------------------------------------- CRIAÇÃO DOS MODELOS/TABELAS -----------------------------------------


class Funcionario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Funcionário',
        default='Funcionário Padrão',  # Valor padrão
    )
    data_nascimento = models.DateField(
        verbose_name='Data de nascimento',
    )
    cpf = models.CharField(
        max_length=80,
        verbose_name='CPF do Funcionário',
        unique=True,
        help_text='Login do Funcionário',
    )
    email = models.EmailField(
        verbose_name='E-mail do Funcionário',
        unique=True,
        max_length=255,
    )
    cargo = models.SmallIntegerField(
        verbose_name='Cargo do Funcionário',
        choices=CARGOS,
        default=0,
    )
    numero_identificacao = models.UUIDField(
        default=uuid.uuid4,
        verbose_name='Identificador Único',
        unique=True,
    )
    supervisor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='subordinados'
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = FuncionarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf', 'nome', 'data_nascimento']

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    def __str__(self):
        return self.nome

    def has_perm(self, perm, obj=None):
        """Verifica se o funcionário possui uma permissão específica."""
        return True  # ou lógica personalizada

    def has_module_perms(self, app_label):
        """Verifica se o funcionário tem permissões para o módulo."""
        return True  # ou lógica personalizada

class Aviao(models.Model):
    capacidade = models.IntegerField(
        verbose_name='Capacidade do Avião',
        blank=False,
        help_text='Quantidade de pessoas que o avião suporta',
        validators=[MinValueValidator(0), MaxValueValidator(850)],
        default=150,  # Ajuste conforme necessário para a capacidade padrão
    )
    modelo = models.CharField(
        max_length=100,
        verbose_name='Modelo do Avião',
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
        default='Modelo Padrão',  # Valor padrão
    )
    nome_companhia = models.CharField(
        max_length=150,
        verbose_name='Nome da Companhia do Avião',
        validators=[MinLengthValidator(2), MaxLengthValidator(150)],
        default='Companhia Padrão',  # Valor padrão
    )

    class Meta:
        verbose_name = 'Avião'
        verbose_name_plural = 'Aviões'

    def __str__(self):
        return self.nome_companhia

class Piloto(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Piloto',
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
        default='Piloto Padrão',  # Valor padrão
    )
    data_nascimento = models.DateField(
        verbose_name='Data de nascimento',
    )
    email = models.EmailField(
        verbose_name='E-mail do Piloto',
        unique=True,
        max_length=255,
        validators=[MinLengthValidator(5), MaxLengthValidator(255)],
    )
    numero_licenca = models.CharField(
        verbose_name='Número da Licença do Piloto',
        unique=True,
        max_length=20,
        validators=[MinLengthValidator(5), MaxLengthValidator(20), RegexValidator(r'^[a-zA-Z0-9]*$', 'A licença deve conter apenas caracteres alfanuméricos.')],
        default='LICENCA123',  # Valor padrão
    )

    class Meta:
        verbose_name = 'Piloto'
        verbose_name_plural = 'Pilotos'

    def __str__(self):
        return self.nome

class Voo(models.Model):
    origem = models.CharField(
        max_length=100,
        verbose_name='Origem do Voo',
        validators=[MaxLengthValidator(100)],
        default='Desconhecida',  # Valor padrão
    )
    destino = models.CharField(
        max_length=100,
        verbose_name='Destino do Voo',
        validators=[MaxLengthValidator(100)],
        default='Desconhecido',  # Valor padrão
    )
    numero = models.IntegerField(
        verbose_name='Número do Voo',
        validators=[MinValueValidator(1)],
        default=1,
    )
    status = models.SmallIntegerField(
        verbose_name='Status do Voo',
        choices=STATUS,
        default=0,  # Ajuste conforme necessário para o status padrão
    )
    aviao = models.ForeignKey(
        Aviao,
        verbose_name='Avião',
        null=True,
        on_delete=models.SET_NULL
    )
    piloto = models.ForeignKey(
        Piloto,
        verbose_name='Piloto',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = 'Voo'
        verbose_name_plural = 'Voos'

    def __str__(self):
        return f'{self.origem} - {self.destino}'

class Passageiro(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Passageiro',
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
        default='Passageiro Padrão',  # Valor padrão
    )
    data_nascimento = models.DateField(
        verbose_name='Data de nascimento',
    )
    cpf_passaporte = models.CharField(
        max_length=20,
        verbose_name='CPF/Passaporte do Passageiro',
        unique=True,
        blank=False,
        validators=[validar_cpf_passaporte],
    )
    email = models.EmailField(
        verbose_name='E-mail do Passageiro',
        unique=True,
        max_length=255,
        validators=[MinLengthValidator(5), MaxLengthValidator(255), validar_email],
    )
    genero = models.SmallIntegerField(
        verbose_name='Gênero do Passageiro',
        choices=GENEROS,
    )
    nacionalidade = models.CharField(
        verbose_name='Nacionalidade do Passageiro',
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
    )
    frequencia_voos = models.IntegerField(
        verbose_name='Frequência de Vôos',
        null=True,
        blank=True,
        help_text='Quantidade de vezes que o cliente já realizou algum vôo',
        validators=[MinValueValidator(0)],
        default=0,  # Valor padrão
    )

    class Meta:
        verbose_name = 'Passageiro'
        verbose_name_plural = 'Passageiros'

    def __str__(self):
        return self.nome


class Reserva(models.Model):
    data_reserva = models.DateTimeField(
        verbose_name='Data/hora da Reserva',
        validators=[validar_data_reserva],
        default=timezone.now,
    )
    preco = models.FloatField(
        verbose_name='Preço da Reserva',
        validators=[MinValueValidator(0)],
        default=0.0,
    )
    assento = models.IntegerField(
        verbose_name='Assento Reservado',
        validators=[MinValueValidator(1)],
        default=1,
    )
    classe = models.SmallIntegerField(
        verbose_name='Classe da Reserva', choices=CLASSES,
        default=1,
    )
    passageiro = models.ForeignKey(
        Passageiro,
        verbose_name='Passageiro',
        help_text='Passageiro que fez a reserva',
        null=True,
        on_delete=models.SET_NULL
    )
    funcionario = models.ForeignKey(
        Funcionario,
        verbose_name='Funcionário que criou a reserva',
        null=True,
        on_delete=models.SET_NULL
    )
    voo = models.ForeignKey(
        Voo,
        verbose_name='Voo Reservado',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'{self.voo.__str__()}, Data: {self.data_reserva}, Assento: {self.assento}'