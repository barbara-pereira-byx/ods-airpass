import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from ods_airpass.core.choices import CARGOS
from ods_airpass.core.constants import EnumCargos


class Funcionario(AbstractBaseUser):
    unique_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name='Identificador Único',
        editable=False,
        unique=True,
        null=True,
        blank=True,
    )
    cpf = models.CharField(
        max_length=80,
        verbose_name='CPF do Funcionário',
        unique=True,
        blank=False,
        help_text='Login do Funcionário',
    )
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Funcionário',
    )
    email = models.EmailField(
        verbose_name='E-mail do Funcionário',
        unique=True,
        max_length=255,
        blank=True,
        null=True,
    )
    data_nascimento = models.DateField(
        verbose_name='Data de nascimento',
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=30,
        verbose_name='Telefone',
        null=True,
        blank=True,
    )
    cargo = models.SmallIntegerField(
        verbose_name='Cargo do Funcionário', choices=CARGOS, null=True, blank=True
    )
    supervisor = models.ForeignKey(
        'self',
        verbose_name='Gestor',
        symmetrical=False,
        related_name='subordinates',
        blank=True,
        null=True,  # Permite que nem todos os funcionários tenham supervisor
        limit_choices_to={
            'cargo__in': [
                EnumCargos.SUPERVISOR_DE_OPERACOES_DE_RESERVAS,
                EnumCargos.GERENTE_DE_VENDAS,
            ]
        },
        on_delete=models.SET_NULL  # Define comportamento ao deletar o supervisor
    )

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'