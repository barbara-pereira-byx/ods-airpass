from django.db import models

from .voo import Voo


class Piloto(models.Model):
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Piloto',
    )
    data_nascimento = models.DateField(
        verbose_name='Data de nascimento',
    )
    email = models.EmailField(
        verbose_name='E-mail do Piloto',
        unique=True,
        max_length=255,
    )
    numero_licenca = models.CharField(
        verbose_name='Número da Licença do Piloto',
        unique=True,
        max_length=255,
    )
    voos = models.ManyToManyField(
        Voo,
        verbose_name='Voos Realizados',
    )

    class Meta:
        verbose_name = 'Piloto'
        verbose_name_plural = 'Pilotos'