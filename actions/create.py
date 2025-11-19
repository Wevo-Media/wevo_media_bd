class CreateTables:
    """
    Classe responsável por criar todas as tabelas do sistema Wevo Media.
    Baseado no esquema do banco de dados completo.
    """

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def execute(self):
        cursor = self.db_connection.cursor()

        tabelas_sql = [
            # Tabela de Leads
            """
            CREATE TABLE IF NOT EXISTS leads (
                id_lead SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                telefone VARCHAR(20),
                email VARCHAR(100),
                origem VARCHAR(50),
                status_funil VARCHAR(50),
                cpf VARCHAR(14) UNIQUE
            );
            """,

            # Tabela de Clientes
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                telefone VARCHAR(20),
                email VARCHAR(100),
                cpf VARCHAR(14) UNIQUE,
                plano_ativo BOOLEAN DEFAULT FALSE,
                id_lead INT,
                FOREIGN KEY (id_lead) REFERENCES leads (id_lead) ON DELETE SET NULL
            );
            """,

            # Tabela de Suporte
            """
            CREATE TABLE IF NOT EXISTS suporte (
                id_chamado SERIAL PRIMARY KEY,
                nome_pedido VARCHAR(100) NOT NULL,
                responsavel_solicitacao VARCHAR(100),
                descricao TEXT,
                data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                id_cliente INT NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente) ON DELETE CASCADE
            );
            """,

            # Tabela de Usuários (sistema de login)
            """
            CREATE TABLE IF NOT EXISTS usuario (
                cpf VARCHAR(14) PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL,
                perfil VARCHAR(20) DEFAULT 'normal' CHECK (perfil IN ('admin', 'normal'))
            );
            """,

            # Tabela de Projetos
            """
            CREATE TABLE IF NOT EXISTS projeto (
                id_projeto SERIAL PRIMARY KEY,
                nome_projeto VARCHAR(200) NOT NULL,
                descricao TEXT,
                status VARCHAR(50) DEFAULT 'Em andamento'
            );
            """,

            # Tabela de Contratos
            """
            CREATE TABLE IF NOT EXISTS contrato (
                id_contrato SERIAL PRIMARY KEY,
                data_inicio DATE NOT NULL,
                data_termino DATE,
                valor DECIMAL(10, 2) NOT NULL,
                status VARCHAR(50) DEFAULT 'Ativo'
            );
            """,

            # Tabela Financeiro
            """
            CREATE TABLE IF NOT EXISTS financeiro (
                id_financeiro SERIAL PRIMARY KEY,
                descricao VARCHAR(200),
                valor DECIMAL(10, 2) NOT NULL,
                data DATE DEFAULT CURRENT_DATE,
                tipo VARCHAR(50) CHECK (tipo IN ('Receita', 'Despesa'))
            );
            """,

            # Tabela de Tarefas
            """
            CREATE TABLE IF NOT EXISTS tarefas (
                id_tarefas SERIAL PRIMARY KEY,
                responsavel VARCHAR(100),
                status VARCHAR(50) DEFAULT 'Pendente',
                prioridade VARCHAR(20) CHECK (prioridade IN ('Baixa', 'Média', 'Alta')),
                descricao TEXT
            );
            """,

            # Tabela Conta a Pagar
            """
            CREATE TABLE IF NOT EXISTS conta_a_pagar (
                id_conta_pagar SERIAL PRIMARY KEY,
                home_beneficiada VARCHAR(100),
                data_vencimento DATE NOT NULL,
                valor DECIMAL(10, 2) NOT NULL,
                descricao TEXT,
                status VARCHAR(50) DEFAULT 'Pendente'
            );
            """,

            # Tabela Conta a Receber
            """
            CREATE TABLE IF NOT EXISTS conta_a_receber (
                id_conta_receber SERIAL PRIMARY KEY,
                data_recebimento DATE,
                valor DECIMAL(10, 2) NOT NULL,
                descricao TEXT,
                id_cliente INT,
                status VARCHAR(50) DEFAULT 'Pendente',
                FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente) ON DELETE SET NULL
            );
            """,

            # Tabelas de Relacionamento

            # Relacionamento: Cliente FAZ Contrato (N:N)
            """
            CREATE TABLE IF NOT EXISTS cliente_contrato (
                id_cliente INT NOT NULL,
                id_contrato INT NOT NULL,
                PRIMARY KEY (id_cliente, id_contrato),
                FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente) ON DELETE CASCADE,
                FOREIGN KEY (id_contrato) REFERENCES contrato (id_contrato) ON DELETE CASCADE
            );
            """,

            # Relacionamento: Projeto GERA Financeiro (1:N via FK)
            """
            ALTER TABLE financeiro
            ADD COLUMN IF NOT EXISTS id_projeto INT,
            ADD CONSTRAINT fk_financeiro_projeto
            FOREIGN KEY (id_projeto) REFERENCES projeto (id_projeto) ON DELETE SET NULL;
            """,

            # Relacionamento: Usuario PARTICIPA Projeto (N:N)
            """
            CREATE TABLE IF NOT EXISTS usuario_projeto (
                cpf_usuario VARCHAR(14) NOT NULL,
                id_projeto INT NOT NULL,
                PRIMARY KEY (cpf_usuario, id_projeto),
                FOREIGN KEY (cpf_usuario) REFERENCES usuario (cpf) ON DELETE CASCADE,
                FOREIGN KEY (id_projeto) REFERENCES projeto (id_projeto) ON DELETE CASCADE
            );
            """,

            # Relacionamento: Usuario ATOCA Tarefas (N:N)
            """
            CREATE TABLE IF NOT EXISTS usuario_tarefa (
                cpf_usuario VARCHAR(14) NOT NULL,
                id_tarefa INT NOT NULL,
                PRIMARY KEY (cpf_usuario, id_tarefa),
                FOREIGN KEY (cpf_usuario) REFERENCES usuario (cpf) ON DELETE CASCADE,
                FOREIGN KEY (id_tarefa) REFERENCES tarefas (id_tarefas) ON DELETE CASCADE
            );
            """,

            # Relacionamento: Contrato TEM Usuario (responsável)
            """
            ALTER TABLE contrato
            ADD COLUMN IF NOT EXISTS cpf_responsavel VARCHAR(14),
            ADD CONSTRAINT fk_contrato_usuario
            FOREIGN KEY (cpf_responsavel) REFERENCES usuario (cpf) ON DELETE SET NULL;
            """,

            # Relacionamento: Projeto TEM Tarefas
            """
            ALTER TABLE tarefas
            ADD COLUMN IF NOT EXISTS id_projeto INT,
            ADD CONSTRAINT fk_tarefa_projeto
            FOREIGN KEY (id_projeto) REFERENCES projeto (id_projeto) ON DELETE CASCADE;
            """,
        ]

        try:
            for sql_cmd in tabelas_sql:
                cursor.execute(sql_cmd)

            self.db_connection.commit()
            print("Todas as tabelas foram criadas com sucesso!")

        except Exception as e:
            self.db_connection.rollback()
            print(f"Erro ao criar tabelas: {e}")

        finally:
            cursor.close()
