from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group
from admin_interface.models import Theme
from .models import Aviao, Funcionario, Passageiro, Piloto, Reserva, Voo

@admin.action(description='Marcar como Em Andamento')
def marcar_em_andamento(modeladmin, request, queryset):
    queryset.update(status=1)

@admin.action(description='Marcar como Atrasado')
def marcar_atrasado(modeladmin, request, queryset):
    queryset.update(status=2)

@admin.action(description='Marcar como Cancelado')
def marcar_cancelado(modeladmin, request, queryset):
    queryset.update(status=3)

@admin.action(description='Marcar como Concluído')
def marcar_concluido(modeladmin, request, queryset):
    queryset.update(status=4)

class ReservaInline(admin.TabularInline):
    model = Reserva
    extra = 0
    list_display = [
        'data_reserva',
        'preco',
        'assento',
        'classe',
    ]

class FuncionarioAdmin(ImportExportModelAdmin):
    model = Funcionario
    search_fields = ['nome','cpf', 'cargo', 'numero_identificacao']
    inlines = [ReservaInline]
    list_display = [
        'nome',
        'cpf',
        'cargo',
        'supervisor',
        'numero_identificacao',
    ]

class PassageiroAdmin(ImportExportModelAdmin):
    model = Passageiro
    search_fields = ['nome','cpf_passaporte', 'email']
    inlines = [ReservaInline]
    list_display = [
        'nome',
        'cpf_passaporte',
        'frequencia_voos',
    ]

class AviaoInline(admin.TabularInline):
    model = Aviao
    list_display = [
        'nome_companhia',
        'modelo',
        'capacidade',
    ]
    extra = 0

class PilotooInline(admin.TabularInline):
    model = Piloto
    list_display = [
        'nome',
        'numero_licenca',
    ]
    extra = 0

class VooAdmin(ImportExportModelAdmin):
    model = Voo
    search_fields = ['numero','origem', 'destino', 'status']
    inlines = [ReservaInline,
               AviaoInline,
               PilotooInline]
    list_display = [
        'origem',
        'destino',
        'numero',
        'status',
    ]

    actions = [marcar_em_andamento, marcar_atrasado, marcar_cancelado, marcar_concluido]

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['botao_alterar_status_voo'] = True

        return super().changeform_view(
            request,
            object_id=object_id,
            form_url=form_url,
            extra_context=extra_context,
        )

    change_form_template = 'change_form.html'

    extra = 0

admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Voo, VooAdmin)
admin.site.register(Passageiro, PassageiroAdmin)
admin.site.unregister(Group)
admin.site.unregister(Theme)