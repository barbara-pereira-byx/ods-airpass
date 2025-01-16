from .constants import EnumCargos, EnumGenero, EnumClasseVoo, EnumStatusVoo


CARGOS = (
    (EnumCargos.AGENTE_DE_RESERVAS.value, 'Agente de Reservas'),
    (EnumCargos.AGENTE_DE_ATENDIMENTO_AO_CLIENTE.value, 'Agente de Atendimento ao Cliente'),
    (EnumCargos.SUPERVISOR_DE_OPERACOES_DE_RESERVAS.value, 'Supervisor de Operações de Reservas'),
    (EnumCargos.GERENTE_DE_VENDAS.value, 'Gerente de Vendas'),
)

GENEROS = (
    (EnumGenero.MASCULINO.value, 'Masculino'),
    (EnumGenero.FEMININO.value, 'Feminino'),
    (EnumGenero.AGENERO.value, 'Agênero'),
    (EnumGenero.GENDERQUEER.value, 'Genderqueer'),
    (EnumGenero.OUTRO.value, 'Outro'),
    (EnumGenero.PREFIRO_NAO_INFORMAR.value, 'Prefiro não informar'),
)

CLASSES = (
    (EnumClasseVoo.ECONOMICA.value, 'Econômica'),
    (EnumClasseVoo.EXECUTIVA.value, 'Executiva'),
    (EnumClasseVoo.PRIMEIRA_CLASSE.value, 'Primeira Classe'),
)

STATUS = (
    (EnumStatusVoo.AGENDADO.value, 'Agendado'),
    (EnumStatusVoo.CONFIRMADO.value, 'Confirmado'),
    (EnumStatusVoo.ATRASADO.value, 'Atrasado'),
    (EnumStatusVoo.CANCELADO.value, 'Cancelado'),
    (EnumStatusVoo.FINALIZADO.value, 'Finalizado'),
)