from datetime import date
import calendar
from models.vacina import Vacina
from models.periodo_vacinacao import PeriodoVacinacao

class B19(Vacina):
    def calcular_periodo(self, idade, quantidade, data_ultima, sexo, b19_aplicada):
        if sexo == 'M':
            return None

        if quantidade > 0:
            return None

        if idade > 8:
            return None

        hoje = date.today()

        if idade < 3:
            data_inicio = self._adicionar_meses(hoje, 3 - idade)
            data_fim = self._adicionar_meses(hoje, 8 - idade)
        else:
            data_inicio = self._adicionar_meses(hoje, -(idade - 3))
            data_fim = self._adicionar_meses(hoje, 8 - idade)

        return PeriodoVacinacao(None, self, data_inicio, data_fim)

    @staticmethod
    def _adicionar_meses(data_base, meses):
        mes_total = data_base.month + meses
        ano = data_base.year + (mes_total - 1) // 12
        mes = (mes_total - 1) % 12 + 1
        dia = min(data_base.day, calendar.monthrange(ano, mes)[1])
        return date(ano, mes, dia)