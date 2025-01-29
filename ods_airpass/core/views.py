from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404

from .choices import GENEROS, CLASSES, STATUS, CARGOS
from .constants import EnumStatusVoo
from .models import Voo, Reserva
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from datetime import datetime

def home(request):
    # Obtém o horário atual
    current_time = datetime.now()

    # Filtra os voos futuros diretamente da tabela Voo, considerando o campo de data e hora
    upcoming_flights = Voo.objects.filter(horario__gte=current_time).order_by('horario')

    # Renderiza a página com os voos filtrados
    return render(request, 'admin/dashboard.html', {'flights': upcoming_flights})

def funcionarios_admin(request):
    return HttpResponseRedirect(reverse('admin:core_funcionario_changelist'))

def passageiros_admin(request):
    return HttpResponseRedirect(reverse('admin:core_passageiro_changelist'))

def voos_admin(request):
    return HttpResponseRedirect(reverse('admin:core_voo_changelist'))

def index(request):
    return HttpResponseRedirect('/admin')

class CancelarVooView(View):
    def post(self, request, voo_id):
        voo = get_object_or_404(Voo, id=voo_id)
        voo.status = EnumStatusVoo.CANCELADO.value
        voo.save()
        messages.success(
            request, 'Status do Voo foi alterado para CANCELADO!'
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class ConcluirVooView(View):
    def post(self, request, voo_id):
        voo = get_object_or_404(Voo, id=voo_id)
        voo.status = EnumStatusVoo.FINALIZADO.value
        voo.save()
        messages.success(
            request, 'Status do Voo foi alterado para FINALIZADO!'
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class AtrasadoVooView(View):
    def post(self, request, voo_id):
        voo = get_object_or_404(Voo, id=voo_id)
        voo.status = EnumStatusVoo.ATRASADO.value
        voo.save()
        messages.success(
            request, 'Status do Voo foi alterado para ATRASADO!'
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class ConfirmadoVooView(View):
    def post(self, request, voo_id):
        voo = get_object_or_404(Voo, id=voo_id)
        voo.status = EnumStatusVoo.CONFIRMADO.value
        voo.save()
        messages.success(
            request, 'Status do Voo foi alterado para CONFIRMADO!'
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class AgendadoVooView(View):
    def post(self, request, voo_id):
        voo = get_object_or_404(Voo, id=voo_id)
        voo.status = EnumStatusVoo.AGENDADO.value
        voo.save()
        messages.success(
            request, 'Status do Voo foi alterado para AGENDADO!'
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class RelatorioReservasView(View):
    def get(self, request):
        # Recuperando todas as reservas
        reservas = Reserva.objects.select_related('passageiro', 'voo', 'voo__aviao', 'voo__piloto').all()
        data = []

        genero_map = dict(GENEROS)
        classe_map = dict(CLASSES)
        status_map = dict(STATUS)

        for reserva in reservas:
            passageiro = reserva.passageiro
            voo = reserva.voo

            # Montando a linha do relatório
            row = {
                'ID': passageiro.id,
                'NomePassageiro': passageiro.nome,
                'DataNascimento': passageiro.data_nascimento,
                'CPFPasaporte': passageiro.cpf_passaporte,
                'Email': passageiro.email,
                'Genero': genero_map.get(passageiro.genero, 'Desconhecido'),
                'Nacionalidade': passageiro.nacionalidade,
                'FrequenciaVoos': passageiro.frequencia_voos,
                'Assento': reserva.assento,
                'Classe': classe_map.get(reserva.classe, 'Desconhecido'),
                'Preco': reserva.preco,
                'VooOrigem': voo.origem if voo else '',
                'VooDestino': voo.destino if voo else '',
                'VooStatus': status_map.get(voo.status, 'Desconhecido') if voo else 'Desconhecido',
                'VooHorario': voo.horario.strftime('%d/%m/%Y às %H:%M') if voo and voo.horario else '',
                'FuncionarioNome': reserva.funcionario.nome if reserva.funcionario else '',
                'FuncionarioEmail': reserva.funcionario.email if reserva.funcionario else '',
                'FuncionarioDataNascimento': reserva.funcionario.data_nascimento.strftime('%Y-%m-%d') if reserva.funcionario and reserva.funcionario.data_nascimento else '',
                'FuncionarioCPF': reserva.funcionario.cpf if reserva.funcionario else '',
                'FuncionarioCargo': reserva.funcionario.cargo if reserva.funcionario else '',
                'FuncionarioNumeroIdentificacao': str(reserva.funcionario.numero_identificacao) if reserva.funcionario else '',
                'FuncionarioSupervisor': reserva.funcionario.supervisor if reserva.funcionario else '',
                'FuncionarioAtivo': reserva.funcionario.is_active if reserva.funcionario else '',
            }
            data.append(row)

        return render(request, 'relatorio_reservas.html', {'reservas': data})

class RelatorioVoosView(View):
    def get(self, request):
        # Recuperando todos os voos com status específico
        status_filtrados = [EnumStatusVoo.CONFIRMADO.value, EnumStatusVoo.ATRASADO.value, EnumStatusVoo.CANCELADO.value]
        voos = Voo.objects.filter(status__in=status_filtrados).select_related('aviao', 'piloto')

        data = []

        # Mapeamento de status
        status_map = dict(STATUS)

        for voo in voos:
            # Montando a linha do relatório
            row = {
                'Origem': voo.origem,
                'Destino': voo.destino,
                'Numero': voo.numero,
                'Status': status_map.get(voo.status, 'Desconhecido'),  # Converte o status para string
                'Horario': voo.horario.strftime('%d/%m/%Y às %H:%M') if voo.horario else None,
                'AviaoCapacidade': voo.aviao.capacidade if voo.aviao else None,
                'AviaoModelo': voo.aviao.modelo if voo.aviao else None,
                'AviaoNomeCompanhia': voo.aviao.nome_companhia if voo.aviao else None,
                'PilotoNome': voo.piloto.nome if voo.piloto else None,
                'PilotoDataNascimento': voo.piloto.data_nascimento.strftime('%Y-%m-%d') if voo.piloto and voo.piloto.data_nascimento else None,
                'PilotoNumeroLicenca': voo.piloto.numero_licenca if voo.piloto else None,
                'PilotoEmail': voo.piloto.email if voo.piloto else None,
            }
            data.append(row)

        return render(request, 'relatorio_voos.html', {'voos': data})