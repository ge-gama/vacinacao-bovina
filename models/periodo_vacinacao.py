from datetime import date

class PeriodoVacinacao:
    def __init__(self, animal, vacina, data_inicio, data_fim):
        self.animal = animal
        self.vacina = vacina
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.nivel = self._calcular_nivel()

    def _calcular_nivel(self):
        hoje = date.today()

        if hoje < self.data_inicio:
            return "pendente"

        if self.data_fim is not None and hoje > self.data_fim:
            return "atrasado"

        return "no_prazo"