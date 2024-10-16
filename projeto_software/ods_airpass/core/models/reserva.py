from django.db import models
from ..choices import CLASSES


class Reserva(models.Model):
    data_reserva = models.DateTimeField(
        verbose_name='Data/hora da Reserva',
    )
    preco = models.FloatField(
        verbose_name='Preço da Reserva',
    )
    assento = models.IntegerField(
        verbose_name='Assento Reservado',
    )
    classe = models.SmallIntegerField(
        verbose_name='Classe da Reserva', choices=CLASSES
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'