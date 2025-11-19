class AddonsQuery:
    
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def select_leads_clientes_suporte(self):
        """
        Consulta combinando as tabelas leads, clientes e suporte.
        Retorna informações do cliente, do lead original e dos chamados de suporte.
        """
        query = """
        SELECT
            l.id_lead,
            l.nome AS nome_lead,
            c.id_cliente,
            c.nome AS nome_cliente,
            c.email,
            s.id_chamado,
            s.nome_pedido,
            s.descricao,
            s.data_solicitacao
        FROM leads l
        JOIN clientes c ON l.id_lead = c.id_lead
        JOIN suporte s ON c.id_cliente = s.id_cliente
        ORDER BY s.data_solicitacao DESC;
        """

        cursor = self.db_connection.cursor()
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            print("Consulta executada com sucesso.\n")
            for row in results:
                print(row)
            return results
        
        except Exception as e:
            print(f"Erro ao executar consulta com JOIN triplo: {e}")
            return []
        
        finally:
            cursor.close()
