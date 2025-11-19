import psycopg2
from utils.connection_db import ConnectionDB
from actions.insert import InsertQuery
from actions.select import SelectQuery
from actions.delete import DeleteQuery
from actions.update import UpdateQuery
from actions.create import CreateTables
from actions.addons import AddonsQuery


class Main:

    def __init__(self):
        self.connection = ConnectionDB().create_connection()

    def create_database(self):
        """
        Cria o banco de dados 'wevo_media' caso não exista.
        """
        try:
            conn = psycopg2.connect(
                database="postgres",
                user="postgres",
                password="admin",
                host="localhost",
                port="5432"
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'wevo_media';")
            exists = cursor.fetchone()

            if not exists:
                cursor.execute("CREATE DATABASE wevo_media;")
                print("Banco de dados 'wevo_media' criado com sucesso.")
            else:
                print("Banco de dados 'wevo_media' já existe.")

        except Exception as e:
            print(f"Erro ao criar banco: {e}")

        finally:
            cursor.close()
            conn.close()

    def create_tables(self):
        """
        Cria todas as tabelas necessárias no banco de dados usando a classe CreateTables.
        """
        creator = CreateTables(self.connection)
        creator.execute()

    def insert_record(self, table, data):
        """
        Insere um novo registro na tabela especificada.

        Args:
            table (str): Nome da tabela onde o registro será inserido.
            data (dict): Dicionário contendo os dados a serem inseridos.
        """
        query_builder = InsertQuery(table, data)
        query, values = query_builder.build_query()

        with self.connection.cursor() as cursor:
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Registro inserido em '{table}'.")

    def select_records(self, table, columns=None, where=None):
        """
        Seleciona registros de uma tabela específica.

        Args:
            table (str): Nome da tabela para consulta.
            columns (list, optional): Lista de colunas a serem retornadas. Se None, retorna todas as colunas.
            where (dict, optional): Condições para filtrar os registros.

        Returns:
            list: Lista de registros encontrados.
        """
        query_builder = SelectQuery(table, columns, where)
        query = query_builder.build_query()

        with self.connection.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                print(row)
            return rows

    def delete_record(self, table, conditions):
        """
        Remove registros de uma tabela específica com base nas condições fornecidas.

        Args:
            table (str): Nome da tabela onde o registro será removido.
            conditions (dict): Dicionário com as condições para identificar os registros a serem removidos.
        """
        query_builder = DeleteQuery(table, conditions)
        query = query_builder.build_query()

        with self.connection.cursor() as cur:
            cur.execute(query)
            self.connection.commit()
            print(f"Registro removido de '{table}'.")

    def update_record(self, query, params=None):
        """
        Atualiza registros no banco de dados usando uma query SQL personalizada.

        Args:
            query (str): Query SQL de atualização.
            params (tuple, optional): Parâmetros para a query SQL.

        Returns:
            int: Número de linhas afetadas pela atualização.
        """
        updater = UpdateQuery(self.connection)
        rows_affected = updater.execute(query, params)
        print(f"{rows_affected} linha(s) atualizada(s).")


if __name__ == "__main__":
    app = Main()

    # Criação do banco e tabelas
    app.create_database()
    app.create_tables()

    # Inserindo um Lead
    app.insert_record("leads", {
        "nome": "João Silva",
        "telefone": "11988887777",
        "email": "joao@example.com",
        "origem": "Instagram",
        "status_funil": "Novo",
        "cpf": "12345678911"
    })

    # Inserindo um Cliente
    app.insert_record("clientes", {
        "nome": "João Silva",
        "telefone": "11988887777",
        "email": "joao@example.com",
        "cpf": "12345678911",
        "plano_ativo": True,
        "id_lead": 1
    })

    # Inserindo um chamado de Suporte
    app.insert_record("suporte", {
        "nome_pedido": "Erro de acesso",
        "responsavel_solicitacao": "Maria",
        "descricao": "Cliente relata erro ao logar",
        "id_cliente": 1
    })

    # Consulta simples
    print("\n Clientes cadastrados:")
    app.select_records("clientes")

    # Atualização de exemplo
    app.update_record(
        "UPDATE clientes SET plano_ativo = %s WHERE id_cliente = %s",
        (False, 1)
    )

    # Exclusão de exemplo
    app.delete_record("suporte", {"id_chamado": 1})

    print("\n Consulta com tres tabelas")
    from actions.addons import AddonsQuery
    addons = AddonsQuery(app.connection)
    addons.select_leads_clientes_suporte()
