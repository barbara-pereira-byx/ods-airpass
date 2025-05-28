from django.db import models


class Piloto(models.Model):
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Piloto',
    )
    data_nascimento = models.DateField(
        verbose_name='Data de nascimento',
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='E-mail do Piloto',
        unique=True,
        max_length=255,
        blank=True,
        null=True,
    )
    numero_licenca = models.CharField(
        verbose_name='Número da Licença do Piloto',
        unique=True,
        blank=False,
    )

    class Meta:
        verbose_name = 'Piloto'
        verbose_name_plural = 'Pilotos'