from django.db import models
from ods_airpass.core.choices import GENEROS


class Passageiro(models.Model):
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Passageiro',
    )
    data_nascimento = models.DateField(
        verbose_name='Data de nascimento',
        null=True,
        blank=True,
    )
    cpf = models.CharField(
        max_length=80,
        verbose_name='CPF/Passaporte do Passageiro',
        unique=True,
        blank=False,
        help_text='Login do Funcionário',
    )
    email = models.EmailField(
        verbose_name='E-mail do Passageiro',
        unique=True,
        max_length=255,
        blank=True,
        null=True,
    )
    genero = models.SmallIntegerField(
        verbose_name='Gênero do Passageiro', choices=GENEROS, null=True, blank=True
    )
    nascionalidade = models.CharField(
        verbose_name='Nascionalidade do Passageiro',
        unique=True,
        blank=False,
    )
    frequencia_voos = models.IntegerField(
        verbose_name='Frequência de Vôos',
        unique=True,
        blank=False,
        help_text='Quantidade de vezes que o cliente já realizou algum vôo',
    )

    class Meta:
        verbose_name = 'Passageiro'
        verbose_name_plural = 'Passageiros'