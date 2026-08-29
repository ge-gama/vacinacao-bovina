import flet as ft
from datetime import datetime
from db.database import inicializar_banco
from repositories.animal_repository import AnimalRepository
from repositories.vacina_repository import VacinaRepository
from services.gerenciador_alertas import GerenciadorAlertas
from models.animal import Animal
from views.tela_inicial import tela_inicial
from views.formulario_animal import formulario_animal
from views.tela_acompanhamento import tela_acompanhamento

def main(page: ft.Page):
    # 1. Inicializar banco de dados
    inicializar_banco()

    # 2. Carregar dados na memória
    lista_vacinas = VacinaRepository.buscar_todos()
    lista_animais = AnimalRepository.buscar_todos()

    # 3. Criar gerenciador e calcular períodos
    gerenciador = GerenciadorAlertas(lista_animais, lista_vacinas)
    gerenciador.calcular_todos()

    # 4. Helper para SnackBar
    def mostrar_snack(mensagem):
        page.snack_bar = ft.SnackBar(ft.Text(mensagem))
        page.snack_bar.open = True
        page.update()

    # 5. Funções de navegação
    def ir_tela_inicial():
        tela_inicial(page, ir_cadastrar, ir_acompanhar)

    def ir_cadastrar():
        formulario_animal(page, on_salvar, ir_tela_inicial)

    def ir_acompanhar():
        tela_acompanhamento(
            page, lista_animais, gerenciador.dicionario,
            on_aplicar, on_excluir, ir_tela_inicial
        )

    # 6. Callback: Salvar animal
    def on_salvar(nome, data_str, sexo):
        if not nome or not nome.strip():
            mostrar_snack("Nome é obrigatório!")
            return

        if not sexo:
            mostrar_snack("Selecione o sexo do animal!")
            return

        try:
            data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            mostrar_snack("Data inválida!")
            return

        animal = Animal(
            nome=nome.strip(),
            data_nascimento=data_nascimento,
            sexo=sexo,
            aplicacoes={}
        )

        try:
            AnimalRepository.salvar(animal)
            lista_animais.append(animal)
            gerenciador.calcular_todos()
            ir_tela_inicial()
            mostrar_snack(f"{animal.nome} cadastrado com sucesso!")
        except Exception as e:
            mostrar_snack(f"Erro ao salvar: {e}")

    # 7. Callback: Aplicar vacina
    def on_aplicar(animal, vacina):
        gerenciador.marcar_aplicada(animal, vacina)
        ir_acompanhar()
        mostrar_snack(f"Vacina {vacina.nome} aplicada em {animal.nome}!")

    # 8. Callback: Excluir animal
    def on_excluir(animal):
        try:
            AnimalRepository.excluir(animal.id)
            lista_animais.remove(animal)
            gerenciador.calcular_todos()
            ir_acompanhar()
            mostrar_snack(f"{animal.nome} excluído.")
        except Exception as e:
            mostrar_snack(f"Erro ao excluir: {e}")

    # 9. Iniciar
    ir_tela_inicial()

ft.run(main)