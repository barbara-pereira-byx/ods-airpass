from django.contrib import admin, messages
from django.db.models import Sum
from import_export.admin import ExportMixin
from django.contrib.auth.models import Group
from admin_interface.models import Theme
from django import forms
from .choices import GENEROS, CARGOS, STATUS, CLASSES
from .constants import EnumStatusVoo
from .models import Aviao, Funcionario, Passageiro, Piloto, Reserva, Voo
from import_export import fields
from django.core.exceptions import ValidationError
import random
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
        status_filtrados = [EnumStatusVoo.CONFIRMADO.value, EnumStatusVoo.ATRASADO.value, EnumStatusVoo.CANCELADO.value]
        queryset = queryset.filter(status__in=status_filtrados)
        return super().export(queryset=queryset, *args, **kwargs)

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data_reserva', 'preco', 'assento', 'classe', 'passageiro', 'funcionario', 'voo']

    def clean(self):
        cleaned_data = super().clean()
        voo = cleaned_data.get('voo')
        classe = cleaned_data.get('classe')
        assento = cleaned_data.get('assento')

        if voo and voo.aviao:
            capacidade_aviao = voo.aviao.capacidade
            capacidade_por_classe = capacidade_aviao // 3

            # Ignorar a reserva atual ao calcular os assentos reservados
            reserva_atual_id = self.instance.id

            assentos_reservados_na_classe = Reserva.objects.filter(
                voo=voo, classe=classe
            ).exclude(id=reserva_atual_id).aggregate(total_assentos=Sum('assento'))['total_assentos'] or 0

            assentos_totais_reservados = Reserva.objects.filter(
                voo=voo
            ).exclude(id=reserva_atual_id).aggregate(total_assentos=Sum('assento'))['total_assentos'] or 0

            if assentos_reservados_na_classe + assento > capacidade_por_classe:
                raise forms.ValidationError(
                    f"Quantidade de assentos selecionados para essa classe ultrapassa o valor disponível. "
                    f"Quantidade de assentos disponíveis para reserva: {capacidade_por_classe - assentos_reservados_na_classe}."
                )

            if assentos_totais_reservados + assento > capacidade_aviao:
                raise forms.ValidationError(
                    f"Capacidade total do avião está próxima do limite. "
                    f"Quantidade de assentos disponíveis para reserva: {capacidade_aviao - assentos_totais_reservados}."
                )

        return cleaned_data

class ReservaAdmin(admin.ModelAdmin):
    model = Reserva
    form = ReservaForm
    extra = 0
    list_display = [
        'get_nome_passageiro',
        'get_nome_funcionario',
        'get_origem_voo',
        'get_destino_voo',
        'get_status_voo',
        'data_reserva',
        'preco',
        'assento',
        'classe',
    ]
    search_fields = [
        'passageiro__nome',
        'funcionario__nome',
        'voo__origem',
        'voo__destino',
    ]

    def get_nome_passageiro(self, obj):
        return obj.passageiro.nome if obj.passageiro else '-'
    get_nome_passageiro.short_description = 'Nome do Passageiro'

    def get_nome_funcionario(self, obj):
        return obj.funcionario.nome if obj.funcionario else '-'
    get_nome_funcionario.short_description = 'Nome do Funcionário'

    def get_origem_voo(self, obj):
        return obj.voo.origem if obj.voo else '-'
    get_origem_voo.short_description = 'Origem do Voo'

    def get_destino_voo(self, obj):
        return obj.voo.destino if obj.voo else '-'
    get_destino_voo.short_description = 'Destino do Voo'

    def get_status_voo(self, obj):
        return dict(STATUS).get(obj.voo.status, None) if obj.voo else '-'
    get_status_voo.short_description = 'Status do Voo'

    def get_form(self, request, obj=None, **kwargs):
        print('Entrou')
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            total_reservas = Reserva.objects.count()

            base_price = {
                1: 300,
                2: 200,
                3: 100,
            }

            classe = form.base_fields.get('classe')
            print('classe')

            if classe and classe.initial:
                print('Entrou classe')
                print(f'Form Fields: {form.base_fields.keys()}')
                incremento = total_reservas * 1.05

                preco_inicial = random.uniform(
                    base_price.get(int(classe.initial), 100),
                    base_price.get(int(classe.initial), 100) + 50
                ) * incremento

                # Verifique se o campo 'preco' está no formulário antes de definir seu valor inicial
                if 'preco' in form.base_fields:
                    print('Preço')
                    form.base_fields['preco'].initial = round(preco_inicial, 2)

        return form

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            self.message_user(request, str(e), level=messages.WARNING)
        else:
            super().save_model(request, obj, form, change)

class FuncionarioAdmin(admin.ModelAdmin):
    model = Funcionario
    search_fields = ['nome','cpf', 'cargo', 'numero_identificacao']
    list_display = [
        'nome',
        'cpf',
        'cargo',
        'supervisor',
        'numero_identificacao',
        'email'
    ]


class PassageiroAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PassageiroResource
    search_fields = ['nome', 'cpf_passaporte', 'email']
    list_display = [
        'nome',
        'cpf_passaporte',
        'frequencia_voos',
        'email',
        'data_nascimento',
        'nacionalidade',
    ]


class AviaoAdmin(admin.ModelAdmin):
    model = Aviao
    list_display = [
        'nome_companhia',
        'modelo',
        'capacidade',
    ]
    search_fields = [
        'nome_companhia',
        'modelo',
    ]
    extra = 0

class PilotooAdmin(admin.ModelAdmin):
    model = Piloto
    list_display = [
        'nome',
        'numero_licenca',
        'email',
        'data_nascimento'
    ]
    search_fields = [
        'nome',
        'numero_licenca',
    ]
    extra = 0

class VooAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = VooResource
    model = Voo
    search_fields = [
        'numero',
        'origem',
        'destino',
        'status',
        'aviao__nome_companhia',
        'aviao__modelo',
        'piloto__nome',
        'piloto__numero_licenca'
    ]
    list_display = [
        'origem',
        'destino',
        'numero',
        'status',
        'get_piloto_nome',
        'get_piloto_numero_licenca',
        'get_nome_companhia',
    ]

    def get_nome_companhia(self, obj):
        return obj.aviao.nome_companhia if obj.aviao else '-'
    get_nome_companhia.short_description = 'Nome da Companhia'

    def get_piloto_nome(self, obj):
        return obj.piloto.nome if obj.piloto else '-'
    get_piloto_nome.short_description = 'Nome do Piloto'

    def get_piloto_numero_licenca(self, obj):
        return obj.piloto.numero_licenca if obj.piloto else '-'
    get_piloto_numero_licenca.short_description = 'Número da Licença do Piloto'

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
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Aviao, AviaoAdmin)
admin.site.register(Piloto, PilotooAdmin)
admin.site.unregister(Group)
admin.site.unregister(Theme)