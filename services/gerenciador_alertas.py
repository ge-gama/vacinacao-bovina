from models.b19 import B19
from repositories.animal_repository import AnimalRepository

class GerenciadorAlertas:
    def __init__(self, lista_animais, lista_vacinas):
        self.lista_animais = lista_animais
        self.lista_vacinas = lista_vacinas
        self.dicionario = {}

        self.id_b19 = None
        for vacina in lista_vacinas:
            if isinstance(vacina, B19):
                self.id_b19 = vacina.id
                break

    def calcular_todos(self):
        self.dicionario = {}

        for animal in self.lista_animais:
            periodos = []
            for vacina in self.lista_vacinas:
                datas = animal.aplicacoes.get(vacina.id, [])
                quantidade = len(datas)
                data_ultima = datas[-1] if datas else None
                idade = animal.calcular_idade_meses()
                b19_aplicada = (
                    len(animal.aplicacoes.get(self.id_b19, [])) > 0
                    if self.id_b19 else False
                )

                periodo = vacina.calcular_periodo(
                    idade=idade,
                    quantidade=quantidade,
                    data_ultima=data_ultima,
                    sexo=animal.sexo,
                    b19_aplicada=b19_aplicada
                )

                if periodo is not None:
                    periodo.animal = animal
                    periodos.append(periodo)

            self.dicionario[animal] = periodos

    def marcar_aplicada(self, animal, vacina):
        animal.marcar_aplicada(vacina.id)
        AnimalRepository.atualizar(animal)
        self.calcular_todos()