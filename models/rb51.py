from datetime import date
import calendar
from models.vacina import Vacina
from models.periodo_vacinacao import PeriodoVacinacao

class RB51(Vacina):
    def calcular_periodo(self, idade, quantidade, data_ultima, sexo, b19_aplicada):
        if sexo == 'M':
            return None

        if quantidade > 0:
            return None

        if b19_aplicada:
            return None

        if idade <= 8:
            return None

        hoje = date.today()
        data_inicio = self._adicionar_meses(hoje, -(idade - 8))
        data_fim = None

        return PeriodoVacinacao(None, self, data_inicio, data_fim)

    @staticmethod
    def _adicionar_meses(data_base, meses):
        mes_total = data_base.month + meses
        ano = data_base.year + (mes_total - 1) // 12
        mes = (mes_total - 1) % 12 + 1
        dia = min(data_base.day, calendar.monthrange(ano, mes)[1])
        return date(ano, mes, dia)