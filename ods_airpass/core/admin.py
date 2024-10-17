from django.contrib import admin

from .models import Aviao, Funcionario, Passageiro, Piloto, Reserva, Voo


class ReservaInline(admin.TabularInline):
    model = Reserva
    extra = 0
    list_display = [
        'data_reserva',
        'preco',
        'assento',
        'classe',
    ]

class FuncionarioAdmin(admin.ModelAdmin):
    model = Funcionario
    inlines = [ReservaInline]
    list_display = [
        'nome',
        'cpf',
        'cargo',
        'supervisor',
        'numero_identificacao',
    ]

class PassageiroAdmin(admin.ModelAdmin):
    model = Passageiro
    inlines = [ReservaInline]
    list_display = [
        'nome',
        'cpf_passaporte',
        'frequencia_voos',
    ]

class VooInline(admin.TabularInline):
    model = Voo
    inlines = [ReservaInline]
    list_display = [
        'origem',
        'destino',
        'numero',
        'status',
    ]
    extra = 0

class AviaoAdmin(admin.ModelAdmin):
    model = Aviao
    inlines = [VooInline]
    list_display = [
        'nome_companhia',
        'modelo',
        'capacidade',
    ]

class PilotooAdmin(admin.ModelAdmin):
    model = Piloto
    inlines = [VooInline]
    list_display = [
        'nome',
        'numero_licenca',
    ]

admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Aviao, AviaoAdmin)
admin.site.register(Piloto, PilotooAdmin)
admin.site.register(Passageiro, PassageiroAdmin)