# Guia Rápido - Sistema Wevo Media

## Instalação Rápida

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Configure o PostgreSQL

Certifique-se de que o PostgreSQL está instalado e rodando. Ajuste o arquivo `.env` se necessário:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=wevo_media
DB_USER=postgres
DB_PASSWORD=admin
```

### 3. Execute o setup inicial

```bash
python setup_inicial.py
```

Este script irá:
- Criar o banco de dados `wevo_media`
- Executar migrations do Django (tabelas do sistema)
- Criar todas as tabelas personalizadas
- Criar um usuário administrador padrão

### 4. Inicie o servidor

```bash
python manage.py runserver
```

### 5. Acesse o sistema

Abra seu navegador em: `http://localhost:8000`

**Credenciais padrão:**
- E-mail: `admin@wevomedia.com`
- Senha: `admin123`

## Estrutura do Sistema

### Módulos Disponíveis

1. **Leads** - Gerenciamento de leads e prospects
2. **Clientes** - Cadastro e gerenciamento de clientes
3. **Suporte** - Chamados e tickets de suporte
4. **Projetos** - Gestão de projetos
5. **Tarefas** - Tarefas relacionadas aos projetos
6. **Contratos** - Contratos com clientes
7. **Financeiro** - Controle de receitas e despesas
8. **Contas a Pagar** - Gestão de contas a pagar
9. **Contas a Receber** - Gestão de contas a receber
10. **Usuários** - Gerenciamento de usuários (apenas Admin)

### Consultas Especiais

Acesse o menu **Consultas Especiais** para visualizar:

1. **Clientes com Chamados Acima da Média** (SELECT Aninhado)
2. **Projetos com Tarefas de Alta Prioridade** (SELECT Aninhado)
3. **Resumo Financeiro por Projeto** (Funções de Grupo)
4. **Estatísticas de Suporte** (Funções de Grupo)
5. **Contas Pendentes** (UNION)
6. **CPFs em Comum** (INTERSECT)

## Perfis de Usuário

### Admin
- Acesso total ao sistema
- Pode criar, editar e **deletar** qualquer registro
- Pode gerenciar outros usuários
- Acesso a todas as funcionalidades

### Normal
- Pode visualizar e editar registros
- **Não pode deletar** registros
- Não tem acesso à gestão de usuários

## Comandos Úteis

### Criar novo usuário via Python

```python
from core.auth import criar_usuario

criar_usuario(
    cpf="12345678900",
    nome="João Silva",
    email="joao@example.com",
    senha="senha123",
    perfil="normal"  # ou "admin"
)
```

### Acessar o shell do Django

```bash
python manage.py shell
```

### Executar comandos SQL diretos

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM leads LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
```

## Solução de Problemas

### Erro de conexão com o banco

1. Verifique se o PostgreSQL está rodando
2. Confirme as credenciais no arquivo `.env`
3. Teste a conexão manual ao PostgreSQL:

```bash
psql -U postgres -h localhost
```

### Erro ao executar migrations

Como usamos `managed=False` nos models, as tabelas são criadas pelo script `create.py`. Se necessário, recrie as tabelas:

```python
python main.py  # Ou execute setup_inicial.py novamente
```

### Porta 8000 já está em uso

Execute o servidor em outra porta:

```bash
python manage.py runserver 8080
```

## Estrutura de Arquivos Importantes

```
wevo_media_bd/
├── setup_inicial.py           # Script de configuração inicial
├── manage.py                  # Gerenciamento Django
├── requirements.txt           # Dependências Python
├── README.md                  # Documentação completa
├── GUIA_RAPIDO.md            # Este arquivo
├── .env                       # Configurações (não comitar!)
├── actions/
│   └── create.py             # Criação das tabelas
├── core/
│   ├── models.py             # Models Django
│   ├── views.py              # Views principais
│   ├── views_crud.py         # Views CRUD
│   ├── views_queries.py      # Consultas especiais
│   ├── urls.py               # URLs da aplicação
│   └── auth.py               # Sistema de autenticação
├── templates/                 # Templates HTML
└── wevo_media_project/
    └── settings.py           # Configurações Django
```

## Dicas de Uso

1. **Primeiro cadastro**: Comece cadastrando alguns Leads, depois converta-os em Clientes
2. **Projetos**: Ao criar um projeto, você pode associar tarefas a ele
3. **Financeiro**: Vincule registros financeiros a projetos para melhor controle
4. **Consultas**: Use as consultas especiais para gerar relatórios gerenciais

## Próximos Passos

1. Cadastre leads e clientes de teste
2. Crie alguns projetos
3. Adicione tarefas aos projetos
4. Registre lançamentos financeiros
5. Explore as consultas especiais

Para documentação completa, consulte o arquivo `README.md`.
