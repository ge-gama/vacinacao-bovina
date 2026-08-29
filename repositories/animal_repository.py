import json
import sqlite3
from datetime import date, datetime
from models.animal import Animal
from db.database import get_connection

class AnimalRepository:

    @staticmethod
    def _serializar_aplicacoes(aplicacoes):
        serializado = {}
        for vacina_id, datas in aplicacoes.items():
            serializado[str(vacina_id)] = [
                d.isoformat() if isinstance(d, date) else d for d in datas
            ]
        return json.dumps(serializado)

    @staticmethod
    def _desserializar_aplicacoes(json_str):
        if not json_str or json_str == '{}':
            return {}
        bruto = json.loads(json_str)
        desserializado = {}
        for vacina_id, datas in bruto.items():
            desserializado[int(vacina_id)] = [
                datetime.strptime(d, "%Y-%m-%d").date() if isinstance(d, str) else d
                for d in datas
            ]
        return desserializado

    @staticmethod
    def salvar(animal):
        animal.validar_dados()
        conexao = None
        try:
            conexao = get_connection()
            cursor = conexao.cursor()
            cursor.execute(
                """INSERT INTO animal (nome, data_nascimento, sexo, aplicacoes)
                   VALUES (?, ?, ?, ?)""",
                (animal.nome, animal.data_nascimento, animal.sexo,
                 AnimalRepository._serializar_aplicacoes(animal.aplicacoes))
            )
            conexao.commit()
            animal.id = cursor.lastrowid
            return animal
        except sqlite3.Error as erro:
            if conexao:
                conexao.rollback()
            print(f"Erro ao salvar animal: {erro}")
            raise
        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def atualizar(animal):
        conexao = None
        try:
            conexao = get_connection()
            cursor = conexao.cursor()
            cursor.execute(
                """UPDATE animal
                   SET nome = ?, data_nascimento = ?, sexo = ?, aplicacoes = ?
                   WHERE id = ?""",
                (animal.nome, animal.data_nascimento, animal.sexo,
                 AnimalRepository._serializar_aplicacoes(animal.aplicacoes),
                 animal.id)
            )
            conexao.commit()
        except sqlite3.Error as erro:
            if conexao:
                conexao.rollback()
            print(f"Erro ao atualizar animal: {erro}")
            raise
        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def excluir(animal_id):
        conexao = None
        try:
            conexao = get_connection()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM animal WHERE id = ?", (animal_id,))
            conexao.commit()
        except sqlite3.Error as erro:
            if conexao:
                conexao.rollback()
            print(f"Erro ao excluir animal: {erro}")
            raise
        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def buscar_todos():
        conexao = None
        try:
            conexao = get_connection()
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM animal ORDER BY nome")
            linhas = cursor.fetchall()
            animais = []
            for linha in linhas:
                aplicacoes = AnimalRepository._desserializar_aplicacoes(
                    linha["aplicacoes"]
                )
                animal = Animal(
                    id=linha["id"],
                    nome=linha["nome"],
                    data_nascimento=linha["data_nascimento"],
                    sexo=linha["sexo"],
                    aplicacoes=aplicacoes
                )
                animais.append(animal)
            return animais
        except sqlite3.Error as erro:
            print(f"Erro ao buscar animais: {erro}")
            raise
        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def buscar_por_id(animal_id):
        conexao = None
        try:
            conexao = get_connection()
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM animal WHERE id = ?", (animal_id,))
            linha = cursor.fetchone()
            if linha is None:
                return None
            aplicacoes = AnimalRepository._desserializar_aplicacoes(
                linha["aplicacoes"]
            )
            return Animal(
                id=linha["id"],
                nome=linha["nome"],
                data_nascimento=linha["data_nascimento"],
                sexo=linha["sexo"],
                aplicacoes=aplicacoes
            )
        except sqlite3.Error as erro:
            print(f"Erro ao buscar animal por id: {erro}")
            raise
        finally:
            if conexao:
                conexao.close()