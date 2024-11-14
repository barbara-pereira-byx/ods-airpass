from django.contrib import admin
from import_export.admin import ExportMixin
from django.contrib.auth.models import Group
from admin_interface.models import Theme
from import_export.results import RowResult
from .choices import GENEROS, CARGOS, STATUS, CLASSES
from .constants import EnumStatusVoo
from .models import Aviao, Funcionario, Passageiro, Piloto, Reserva, Voo
from import_export import fields

from import_export import resources
from import_export.fields import Field
from tablib import Dataset

class PassageiroResource(resources.ModelResource):
    # Definindo os campos do passageiro
    id = Field(attribute='id', column_name='Passageiro - ID')
    nome = Field(attribute='nome', column_name='Passageiro - Nome do Passageiro')
    data_nascimento = Field(attribute='data_nascimento', column_name='Passageiro - Data de Nascimento')
    cpf_passaporte = Field(attribute='cpf_passaporte', column_name='Passageiro - CPF/Passaporte')
    email = Field(attribute='email', column_name='Passageiro - Email do Passageiro')
    genero = Field(attribute='genero', column_name='Passageiro - Gênero')
    nacionalidade = Field(attribute='nacionalidade', column_name='Passageiro - Nacionalidade')
    frequencia_voos = Field(attribute='frequencia_voos', column_name='Passageiro - Frequência de Voos')

    class Meta:
        model = Passageiro
        fields = (
            'id',  # Inclui o campo 'id' na exportação
            'nome',
            'data_nascimento',
            'cpf_passaporte',
            'email',
            'genero',
            'nacionalidade',
            'frequencia_voos',
        )

    def export(self, queryset=None, *args, **kwargs):
        # Exportando o dataset original
        dataset = super().export(queryset=queryset, *args, **kwargs)
        new_data = []

        # Headers completos incluindo todos os campos de Passageiro, Reserva e Funcionário
        headers = dataset.headers + [
            'Assento', 'Classe', 'Preço', 'Data da Reserva',
            'Voo - Origem', 'Voo - Destino', 'Voo - Status',
            'Funcionário - Nome', 'Funcionário - Email', 'Funcionário - Data de Nascimento',
            'Funcionário - CPF', 'Funcionário - Cargo', 'Funcionário - Número de Identificação',
            'Funcionário - Supervisor', 'Funcionário - Ativo?'
        ]

        # Dicionários para mapear os valores numéricos aos nomes textuais
        genero_map = dict(GENEROS)
        classe_map = dict(CLASSES)
        status_map = dict(STATUS)
        cargo_map = dict(CARGOS)

        # Iterando sobre cada linha do dataset exportado
        for row in dataset.dict:
            passageiro_data = row.copy()

            # Convertendo o gênero do passageiro
            genero_valor = passageiro_data.get('Passageiro - Gênero')
            try:
                genero_valor = int(genero_valor) if genero_valor is not None else None
            except ValueError:
                genero_valor = None  # Trata casos de valores inesperados
            passageiro_data['Passageiro - Gênero'] = genero_map.get(genero_valor, 'Desconhecido')

            # Obtendo o ID do passageiro
            passageiro_id = passageiro_data.get('Passageiro - ID')

            # Verificando se o ID está disponível
            if not passageiro_id:
                continue  # Ignora a linha se o ID do passageiro estiver ausente

            # Buscando reservas associadas ao passageiro
            reservas = Reserva.objects.filter(passageiro_id=passageiro_id)

            # Criando uma nova linha para cada reserva
            for reserva in reservas:
                new_row = passageiro_data.copy()

                # Adicionando os dados da reserva e do funcionário à linha, com conversão dos nomes
                new_row.update({
                    'Assento': reserva.assento,
                    'Classe': classe_map.get(reserva.classe, 'Desconhecido'),
                    'Preço': reserva.preco,
                    'Data da Reserva': reserva.data_reserva,
                    'Voo - Origem': reserva.voo.origem,
                    'Voo - Destino': reserva.voo.destino,
                    'Voo - Status': status_map.get(reserva.voo.status, 'Desconhecido'),
                    'Funcionário - Nome': reserva.funcionario.nome if reserva.funcionario else '',
                    'Funcionário - Email': reserva.funcionario.email if reserva.funcionario else '',
                    'Funcionário - Data de Nascimento': reserva.funcionario.data_nascimento if reserva.funcionario else '',
                    'Funcionário - CPF': reserva.funcionario.cpf if reserva.funcionario else '',
                    'Funcionário - Cargo': cargo_map.get(reserva.funcionario.cargo,
                                                         'Desconhecido') if reserva.funcionario else '',
                    'Funcionário - Número de Identificação': str(
                        reserva.funcionario.numero_identificacao) if reserva.funcionario else '',
                    'Funcionário - Supervisor': reserva.funcionario.supervisor if reserva.funcionario else '',
                    'Funcionário - Ativo?': reserva.funcionario.is_active if reserva.funcionario else '',
                })
                new_data.append(new_row)

        # Criando um novo dataset para incluir os dados ajustados
        new_dataset = Dataset()
        new_dataset.headers = headers
        for row in new_data:
            new_dataset.append([row.get(header, '') for header in headers])

        return new_dataset


class VooResource(resources.ModelResource):
    # Campos do Voo
    origem = fields.Field(column_name='Origem')
    destino = fields.Field(column_name='Destino')
    numero = fields.Field(column_name='Número do Voo')
    status = fields.Field(column_name='Status')

    # Campos de Avião
    aviao_capacidade = fields.Field(column_name='Avião - Capacidade')
    aviao_modelo = fields.Field(column_name='Avião - Modelo')
    aviao_nome_companhia = fields.Field(column_name='Avião - Nome da Companhia')

    # Campos de Piloto
    piloto_nome = fields.Field(column_name='Piloto - Nome')
    piloto_data_nascimento = fields.Field(column_name='Piloto - Data de Nascimento')
    piloto_numero_licenca = fields.Field(column_name='Piloto - Número de Licença')
    piloto_email = fields.Field(column_name='Piloto - E-mail')

    class Meta:
        model = Voo
        fields = (
            'origem', 'destino', 'numero', 'status',
            'aviao_capacidade', 'aviao_modelo', 'aviao_nome_companhia',
            'piloto_nome', 'piloto_data_nascimento', 'piloto_numero_licenca', 'piloto_email',
        )

    def dehydrate_origem(self, obj):
        return obj.origem if obj else None

    def dehydrate_destino(self, obj):
        return obj.destino if obj else None

    def dehydrate_numero(self, obj):
        return obj.numero if obj else None

    def dehydrate_status(self, obj):
        if obj and obj.status is not None:
            return dict(STATUS).get(obj.status, None)
        return None

    def dehydrate_aviao_capacidade(self, obj):
        avioes = Aviao.objects.filter(voo=obj)
        return ', '.join(str(aviao.capacidade) for aviao in avioes) if avioes.exists() else None

    def dehydrate_aviao_modelo(self, obj):
        avioes = Aviao.objects.filter(voo=obj)
        return ', '.join(aviao.modelo for aviao in avioes) if avioes.exists() else None

    def dehydrate_aviao_nome_companhia(self, obj):
        avioes = Aviao.objects.filter(voo=obj)
        return ', '.join(aviao.nome_companhia for aviao in avioes) if avioes.exists() else None

    def dehydrate_piloto_nome(self, obj):
        pilotos = Piloto.objects.filter(voo=obj)
        return ', '.join(piloto.nome for piloto in pilotos) if pilotos.exists() else None

    def dehydrate_piloto_data_nascimento(self, obj):
        pilotos = Piloto.objects.filter(voo=obj)
        return ', '.join(
            piloto.data_nascimento.strftime('%Y-%m-%d') for piloto in pilotos) if pilotos.exists() else None

    def dehydrate_piloto_numero_licenca(self, obj):
        pilotos = Piloto.objects.filter(voo=obj)
        return ', '.join(piloto.numero_licenca for piloto in pilotos) if pilotos.exists() else None

    def dehydrate_piloto_email(self, obj):
        pilotos = Piloto.objects.filter(voo=obj)
        return ', '.join(piloto.email for piloto in pilotos) if pilotos.exists() else None

    def export(self, queryset=None, *args, **kwargs):
        # Filtro para incluir apenas os voos com status específico
        status_filtrados = [EnumStatusVoo.EM_ANDAMENTO.value, EnumStatusVoo.ATRASADO.value, EnumStatusVoo.CANCELADO.value]
        queryset = queryset.filter(status__in=status_filtrados)
        return super().export(queryset=queryset, *args, **kwargs)


class ReservaInline(admin.TabularInline):
    model = Reserva
    extra = 1
    list_display = [
        'data_reserva',
        'preco',
        'assento',
        'classe',
    ]

class FuncionarioAdmin(admin.ModelAdmin):
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


class PassageiroAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PassageiroResource
    search_fields = ['nome', 'cpf_passaporte', 'email']
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
    extra = 1

class PilotooInline(admin.TabularInline):
    model = Piloto
    list_display = [
        'nome',
        'numero_licenca',
    ]
    extra = 1

class VooAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = VooResource
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