from django.db import models

from ..choices import STATUS
from .reserva import Reserva


class Voo(models.Model):
    data_reserva = models.DateTimeField(
        verbose_name='Data/hora da Reserva',
    )
    origem = models.CharField(
        max_length=255,
        verbose_name='Origem do Voo',
    )
    destino = models.CharField(
        max_length=255,
        verbose_name='Destino do Voo',
    )
    numero = models.IntegerField(
        verbose_name='Número do Voo',
    )
    status = models.SmallIntegerField(
        verbose_name='Status do Voo',
        choices=STATUS,
    )
    reservas_do_voo = models.ManyToManyField(
        Reserva,
        verbose_name='Reservas para o Voo',
    )

    class Meta:
        verbose_name = 'Voo'
        verbose_name_plural = 'Voo'