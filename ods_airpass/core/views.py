from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404
from .constants import EnumStatusVoo
from .models import Voo
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