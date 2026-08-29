from abc import ABC, abstractmethod
from datetime import date
from models.periodo_vacinacao import PeriodoVacinacao

class Vacina(ABC):
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    @abstractmethod
    def calcular_periodo(self, idade, quantidade, data_ultima, sexo, b19_aplicada):
        pass