from .constants import EnumCargos, EnumGenero, EnumClasseVoo, EnumStatusVoo


CARGOS = (
    (EnumCargos.AGENTE_DE_RESERVAS, 'Agente de Reservas'),
    (EnumCargos.AGENTE_DE_ATENDIMENTO_AO_CLIENTE, 'Agente de Atendimento ao Cliente'),
    (EnumCargos.SUPERVISOR_DE_OPERACOES_DE_RESERVAS, 'Supervisor de Operações de Reservas'),
    (EnumCargos.GERENTE_DE_VENDAS, 'Gerente de Vendas'),
)

GENEROS = (
    (EnumGenero.MASCULINO, 'Masculino'),
    (EnumGenero.FEMININO, 'Feminino'),
    (EnumGenero.AGENERO, 'Agênero'),
    (EnumGenero.GENDERQUEER, 'Genderqueer'),
    (EnumGenero.OUTRO, 'Outro'),
    (EnumGenero.PREFIRO_NAO_INFORMAR, 'Prefiro não informar'),
)

CLASSES = (
    (EnumClasseVoo.ECONOMICA, 'Econômica'),
    (EnumClasseVoo.EXECUTIVA, 'Executiva'),
    (EnumClasseVoo.PRIMEIRA_CLASSE, 'Primeira Classe'),
    (EnumClasseVoo.CLASSE_BUSINESS, 'Classe Business'),
    (EnumClasseVoo.CLASSE_ECONOMICA_SUPERIOR, 'Classe Econômica Superior'),
)

STATUS = (
    (EnumStatusVoo.AGENDADO, 'Agendado'),
    (EnumStatusVoo.EM_ANDAMENTO, 'Em Andamento'),
    (EnumStatusVoo.ATRASADO, 'Atrasado'),
    (EnumStatusVoo.CANCELADO, 'Cancelado'),
    (EnumStatusVoo.CONCLUIDO, 'Concluido'),
)