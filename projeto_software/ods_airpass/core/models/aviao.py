from django.db import models

from .voo import Voo


class Aviao(models.Model):
    capacidade = models.IntegerField(
        verbose_name='Capacidade do Avião',
        blank=False,
        help_text='Quantidade de pessoas que o avião suporta',
    )
    modelo = models.CharField(
        max_length=255,
        verbose_name='Modelo do Avião',
    )
    nome_companhia = models.CharField(
        max_length=255,
        verbose_name='Nome da Companhia do Avião',
    )
    voos = models.ManyToManyField(
        Voo,
        verbose_name='Voos Realizados',
    )

    class Meta:
        verbose_name = 'Avião'
        verbose_name_plural = 'Aviões'