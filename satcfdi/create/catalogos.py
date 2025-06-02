from enum import StrEnum


class EstadoComprobante(StrEnum):
    CANCELADO = 'Cancelado'
    VIGENTE = 'Vigente'
    TODOS = 'Todos'