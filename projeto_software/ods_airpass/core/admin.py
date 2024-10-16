from django.contrib import admin

from .models.aviao import Aviao
from .models.funcionario import Funcionario
from .models.passageiro import Passageiro
from .models.piloto import Piloto
from .models.reserva import Reserva
from .models.voo import Voo


class AviaoAdmin(admin.ModelAdmin):
    model = Aviao

class FuncionarioAdmin(admin.ModelAdmin):
    model = Funcionario

class PassageiroAdmin(admin.ModelAdmin):
    model = Passageiro

class PilotooAdmin(admin.ModelAdmin):
    model = Piloto

class ReservaAdmin(admin.ModelAdmin):
    model = Reserva

class VooAdmin(admin.ModelAdmin):
    model = Voo

admin.site.register(Aviao, AviaoAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Passageiro, PassageiroAdmin)
admin.site.register(Piloto, PilotooAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Voo, VooAdmin)