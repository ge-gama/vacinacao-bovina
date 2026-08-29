from datetime import date, datetime

class Animal:
    def __init__(self, id, nome, data_nascimento, sexo, aplicacoes=None):
        self.id = id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.aplicacoes = aplicacoes if aplicacoes is not None else {}

    def validar_dados(self):
        if not self.nome or not self.nome.strip():
            raise ValueError("Nome nao pode ser vazio")

        try:
            data = datetime.strptime(self.data_nascimento, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Data de nascimento invalida (formato esperado: YYYY-MM-DD)")

        if data > date.today():
            raise ValueError("Data de nascimento nao pode ser futura")

        if self.sexo not in ('M', 'F'):
            raise ValueError("Sexo deve ser 'M' ou 'F'")

    def calcular_idade_meses(self):
        data_nasc = datetime.strptime(self.data_nascimento, "%Y-%m-%d").date()
        hoje = date.today()
        meses = (hoje.year - data_nasc.year) * 12 + (hoje.month - data_nasc.month)
        if hoje.day < data_nasc.day:
            meses -= 1
        return meses

    def marcar_aplicada(self, vacina_id):
        if vacina_id not in self.aplicacoes:
            self.aplicacoes[vacina_id] = []
        self.aplicacoes[vacina_id].append(date.today())

    def get_quantidade(self, vacina_id):
        return len(self.aplicacoes.get(vacina_id, []))