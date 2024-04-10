import sqlite3
import pandas as pd
#Cria banco de dados caso ele não exista
def criar_banco_de_dados():
    # Conectar ao banco de dados ou criar se não existir
    conexao = sqlite3.connect('bd/trabalhoFlaskSha256.db')

    # Criar um cursor para interagir com o banco de dados
    cursor = conexao.cursor()

    # Criar a tabela arquivos
    cursor.execute('''CREATE TABLE IF NOT EXISTS arquivos
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hash TEXT NOT NULL, arquivo TEXT NOT NULL)''')

    # Salvar as alterações e fechar a conexão com o banco de dados
    conexao.commit()
    conexao.close()

    print("Banco de dados criado com sucesso.")

#adiciona o hash e o nome do arquivo ao banco
def adicionar_valores(hash, nome_arquivo):
    conexao = sqlite3.connect('bd/trabalhoFlaskSha256.db')
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO arquivos (hash, arquivo) VALUES (?, ?)", (hash, nome_arquivo))

    # Salvar as alterações e fechar a conexão com o banco de dados
    conexao.commit()
    conexao.close()
    print(f"Hash {hash} salvo com sucesso!")

#seleciona um hash especifico do banco de dados, caso ele não exita, retorna None
def selecionar_hash_do_banco(hash):
    conexao = sqlite3.connect('bd/trabalhoFlaskSha256.db')
    cursor = conexao.cursor()
    arquivo = cursor.execute(f"SELECT * FROM arquivos where hash = (?)", (hash,))
    arquivo = arquivo.fetchone()
    conexao.close()
    return arquivo

def selecionar_todos_os_arquivos():
    conexao = sqlite3.connect('bd/trabalhoFlaskSha256.db')
    cursor = conexao.cursor()
    arquivos = f"SELECT * FROM arquivos"
    arquivos = pd.read_sql_query(arquivos, conexao)
    conexao.close()
    return arquivos.to_dict(orient='records')
