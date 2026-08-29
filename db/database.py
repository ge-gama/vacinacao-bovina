import os
import sqlite3

def get_caminho_banco() -> str:
    diretorio_db = os.path.dirname(os.path.abspath(__file__))
    diretorio_raiz = os.path.dirname(diretorio_db)
    return os.path.join(diretorio_raiz, "vacinacao_bovina.db")

def get_connection() -> sqlite3.Connection:
    try:
        caminho_banco = get_caminho_banco()
        conexao = sqlite3.connect(caminho_banco)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON;")
        return conexao
    except sqlite3.Error as erro:
        print(f"Erro ao abrir conexao com o banco de dados: {erro}")
        raise

def criar_tabelas() -> None:
    ddl_animal = """
    CREATE TABLE IF NOT EXISTS animal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento TEXT NOT NULL,
        sexo TEXT NOT NULL CHECK(sexo IN ('M', 'F')),
        aplicacoes TEXT NOT NULL DEFAULT '{}'
    );
    """

    ddl_vacina = """
    CREATE TABLE IF NOT EXISTS vacina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    );
    """

    conexao = None
    try:
        conexao = get_connection()
        cursor = conexao.cursor()
        cursor.execute(ddl_animal)
        cursor.execute(ddl_vacina)
        conexao.commit()
    except sqlite3.Error as erro:
        if conexao:
            conexao.rollback()
        print(f"Erro ao executar criacao de tabelas: {erro}")
        raise
    finally:
        if conexao:
            conexao.close()

def popular_vacinas() -> None:
    vacinas_iniciais = [
        ("Brucelose B19",),
        ("Brucelose RB51",),
        ("Raiva",),
        ("Clostridioses",),
        ("Leptospirose",),
    ]

    conexao = None
    try:
        conexao = get_connection()
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM vacina;")
        quantidade_existente = cursor.fetchone()[0]

        if quantidade_existente == 0:
            cursor.executemany(
                "INSERT INTO vacina (nome) VALUES (?);", vacinas_iniciais
            )
            conexao.commit()
    except sqlite3.Error as erro:
        if conexao:
            conexao.rollback()
        print(f"Erro ao popular catalogo de vacinas: {erro}")
        raise
    finally:
        if conexao:
            conexao.close()

def inicializar_banco() -> None:
    try:
        criar_tabelas()
        popular_vacinas()
    except Exception as erro:
        print(f"Falha durante a inicializacao do banco de dados: {erro}")
        raise