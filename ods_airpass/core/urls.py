"""
URL configuration for ods_airpass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),  # admin deve vir primeiro
    path('', core_views.home, name='home'),  # Página inicial
    path('core/', core_views.home, name='home'),  # Redirecionamento para home
    path('core/relatorio_reservas/', core_views.RelatorioReservasView.as_view(), name='relatorio_reservas'),
    path('core/relatorio_voos/', core_views.RelatorioVoosView.as_view(), name='relatorio_voos'),
    path('cancelar-voo/<int:voo_id>/', core_views.CancelarVooView.as_view(), name='cancelar_voo'),
    path('concluir-voo/<int:voo_id>/', core_views.ConcluirVooView.as_view(), name='concluir_voo'),
    path('atrasado-voo/<int:voo_id>/', core_views.AtrasadoVooView.as_view(), name='atrasado_voo'),
    path('agendado-voo/<int:voo_id>/', core_views.AgendadoVooView.as_view(), name='agendado_voo'),
    path('confirmado-voo/<int:voo_id>/', core_views.ConfirmadoVooView.as_view(), name='confirmado_voo'),
]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]

