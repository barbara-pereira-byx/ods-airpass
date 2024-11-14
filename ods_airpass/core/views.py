from django.contrib import messages
from django.views import View
from django.shortcuts import get_object_or_404
from .constants import EnumStatusVoo
from .models import Voo
from django.http import HttpResponseRedirect

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
        voo.status = EnumStatusVoo.CONCLUIDO.value
        voo.save()
        messages.success(
            request, 'Status do Voo foi alterado para CONCLUIDO!'
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

class EmAndamentoVooView(View):
    def post(self, request, voo_id):
        voo = get_object_or_404(Voo, id=voo_id)
        voo.status = EnumStatusVoo.EM_ANDAMENTO.value
        voo.save()
        messages.success(
            request, 'Status do Voo foi alterado para EM ANDAMENTO!'
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