import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from ..choices import CARGOS
from ..constants import EnumCargos
from .reserva import Reserva


class Funcionario(AbstractBaseUser):
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Funcionário',
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
    reservas_criadas = models.ManyToManyField(
        Reserva,
        verbose_name='Reservas Criadas',
    )

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'