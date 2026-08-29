import sqlite3
from db.database import get_connection
from models.vacina import Vacina
from models.b19 import B19
from models.rb51 import RB51
from models.raiva import Raiva
from models.clostridioses import Clostridioses
from models.leptospirose import Leptospirose

class VacinaRepository:

    MAPEAMENTO = {
        "Brucelose B19": B19,
        "Brucelose RB51": RB51,
        "Raiva": Raiva,
        "Clostridioses": Clostridioses,
        "Leptospirose": Leptospirose,
    }

    @staticmethod
    def buscar_todos():
        conexao = None
        try:
            conexao = get_connection()
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM vacina ORDER BY id")
            linhas = cursor.fetchall()
            vacinas = []
            for linha in linhas:
                nome = linha["nome"]
                classe = VacinaRepository.MAPEAMENTO.get(nome)
                if classe is None:
                    print(f"Vacina nao mapeada: {nome}")
                    continue
                vacinas.append(classe(id=linha["id"], nome=nome))
            return vacinas
        except sqlite3.Error as erro:
            print(f"Erro ao buscar vacinas: {erro}")
            raise
        finally:
            if conexao:
                conexao.close()

    @staticmethod
    def buscar_por_id(vacina_id):
        conexao = None
        try:
            conexao = get_connection()
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM vacina WHERE id = ?", (vacina_id,))
            linha = cursor.fetchone()
            if linha is None:
                return None
            nome = linha["nome"]
            classe = VacinaRepository.MAPEAMENTO.get(nome)
            if classe is None:
                print(f"Vacina nao mapeada: {nome}")
                return None
            return classe(id=linha["id"], nome=nome)
        except sqlite3.Error as erro:
            print(f"Erro ao buscar vacina por id: {erro}")
            raise
        finally:
            if conexao:
                conexao.close()