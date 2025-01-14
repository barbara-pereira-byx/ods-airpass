from enum import Enum

class EnumCargos(Enum):
    AGENTE_DE_RESERVAS = 0
    AGENTE_DE_ATENDIMENTO_AO_CLIENTE = 1
    SUPERVISOR_DE_OPERACOES_DE_RESERVAS = 2
    GERENTE_DE_VENDAS = 3

class EnumGenero(Enum):
    MASCULINO = 0
    FEMININO = 1
    NAO_BINARIO = 2
    AGENERO = 3
    GENDERQUEER = 4
    OUTRO = 5
    PREFIRO_NAO_INFORMAR = 6

class EnumClasseVoo(Enum):
    ECONOMICA = 0
    EXECUTIVA = 1
    PRIMEIRA_CLASSE = 2

class EnumStatusVoo(Enum):
    AGENDADO = 0
    CONFIRMADO = 1
    ATRASADO = 2
    CANCELADO = 3
    FINALIZADO = 4