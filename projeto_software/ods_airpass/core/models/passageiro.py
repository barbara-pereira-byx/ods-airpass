from django.db import models

from .reserva import Reserva
from ..choices import GENEROS


class Passageiro(models.Model):
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Passageiro',
    )
    data_nascimento = models.DateField(
        verbose_name='Data de nascimento',
    )
    cpf_passaporte = models.CharField(
        max_length=80,
        verbose_name='CPF/Passaporte do Passageiro',
        unique=True,
        blank=False,
    )
    email = models.EmailField(
        verbose_name='E-mail do Passageiro',
        unique=True,
        max_length=255,
    )
    genero = models.SmallIntegerField(
        verbose_name='Gênero do Passageiro',
        choices=GENEROS,
    )
    nascionalidade = models.CharField(
        verbose_name='Nascionalidade do Passageiro',
        max_length=255,
    )
    frequencia_voos = models.IntegerField(
        verbose_name='Frequência de Vôos',
        null=True,
        blank=True,
        help_text='Quantidade de vezes que o cliente já realizou algum vôo',
    )
    reserva = models.ManyToManyField(
        Reserva,
        verbose_name='Reserva',
    )

    class Meta:
        verbose_name = 'Passageiro'
        verbose_name_plural = 'Passageiros'