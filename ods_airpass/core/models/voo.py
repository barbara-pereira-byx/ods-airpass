from django.db import models

from ods_airpass.core.choices import CLASSES


class Voo(models.Model):
    data_reserva = models.DateTimeField(
        verbose_name='Data/hora da Reserva',
        null=True,
        blank=True,
    )
    preco = models.FloatField(
        verbose_name='Preço da Reserva',
        blank=True,
        null=True,
    )
    assento = models.IntegerField(
        verbose_name='Assento Reservado',
        blank=True,
        null=True,
        unique=True,
    )
    classe = models.SmallIntegerField(
        verbose_name='Classe da Reserva', choices=CLASSES, null=True, blank=True
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'