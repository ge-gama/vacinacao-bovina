from datetime import date, timedelta
import calendar
from models.vacina import Vacina
from models.periodo_vacinacao import PeriodoVacinacao

class Leptospirose(Vacina):
    def calcular_periodo(self, idade, quantidade, data_ultima, sexo, b19_aplicada):
        hoje = date.today()

        if quantidade == 0:
            if idade < 10:
                data_inicio = self._adicionar_meses(hoje, 10 - idade)
            else:
                data_inicio = self._adicionar_meses(hoje, -(idade - 10))
            data_fim = None

        elif quantidade == 1:
            data_inicio = data_ultima + timedelta(days=30)
            data_fim = data_ultima + timedelta(days=45)

        else:
            data_inicio = data_ultima + timedelta(days=365)
            data_fim = None

        return PeriodoVacinacao(None, self, data_inicio, data_fim)

    @staticmethod
    def _adicionar_meses(data_base, meses):
        mes_total = data_base.month + meses
        ano = data_base.year + (mes_total - 1) // 12
        mes = (mes_total - 1) % 12 + 1
        dia = min(data_base.day, calendar.monthrange(ano, mes)[1])
        return date(ano, mes, dia)