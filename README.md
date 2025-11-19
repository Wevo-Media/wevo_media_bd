# Sistema de Gestão Wevo Media

Sistema completo de gestão desenvolvido com Django e PostgreSQL para gerenciamento de leads, clientes, projetos, contratos, financeiro e suporte.

## Características

- **CRUD Completo** para todas as entidades do sistema
- **Sistema de Autenticação** com perfis de Admin e Usuário Normal
- **Consultas SQL Avançadas**:
  - 2 consultas com SELECT aninhado
  - 2 consultas com funções de grupo (COUNT, SUM, AVG, MAX, MIN)
  - 2 consultas com operadores de conjunto (UNION, INTERSECT)
- **Interface Visual** moderna e responsiva com Bootstrap 5
- **Modularização** de código seguindo boas práticas

## Tecnologias Utilizadas

- **Backend**: Django 4.2.7
- **Banco de Dados**: PostgreSQL
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Python**: 3.8+

## Estrutura do Banco de Dados

O sistema possui as seguintes tabelas:

### Entidades Principais
- **leads** - Gerenciamento de leads
- **clientes** - Cadastro de clientes
- **suporte** - Chamados de suporte
- **usuario** - Usuários do sistema
- **projeto** - Projetos
- **contrato** - Contratos
- **financeiro** - Registros financeiros
- **tarefas** - Tarefas dos projetos
- **conta_a_pagar** - Contas a pagar
- **conta_a_receber** - Contas a receber

### Tabelas de Relacionamento
- **cliente_contrato** - Relacionamento N:N entre Clientes e Contratos
- **usuario_projeto** - Relacionamento N:N entre Usuários e Projetos
- **usuario_tarefa** - Relacionamento N:N entre Usuários e Tarefas

## Instalação e Configuração

### 1. Clone o repositório

```bash
cd wevo_media_bd
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo .env

Ajuste as configurações do banco de dados no arquivo `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=wevo_media
DB_USER=postgres
DB_PASSWORD=admin
```

### 5. Execute o setup inicial

```bash
python setup_inicial.py
```

Este script irá:
- Criar o banco de dados `wevo_media`
- Executar migrations do Django (para tabelas do sistema como django_session, auth, etc.)
- Criar todas as tabelas personalizadas do sistema
- Criar um usuário administrador padrão

**Nota**: O script `setup_inicial.py` deve ser executado APENAS UMA VEZ na primeira instalação. Ele já cria automaticamente o usuário administrador.

### 6. Execute o servidor

```bash
python manage.py runserver
```

Acesse o sistema em: `http://localhost:8000`

## Credenciais Padrão

Após executar o setup inicial:

- **E-mail**: admin@wevomedia.com
- **Senha**: admin123

## Funcionalidades

### 1. Sistema de Autenticação
- Login com **E-mail e senha**
- Registro de novos usuários
- Dois perfis de acesso:
  - **Admin**: Acesso total, incluindo exclusão de registros e gestão de usuários
  - **Normal**: Acesso para visualização e edição (sem exclusão)

### 2. CRUD Completo

Operações de Create, Read, Update e Delete para:

- Leads
- Clientes
- Suporte (Chamados)
- Projetos
- Contratos
- Financeiro
- Tarefas
- Contas a Pagar
- Contas a Receber
- Usuários (apenas Admin)

### 3. Consultas Especiais

#### SELECT Aninhado
1. **Clientes com Chamados Acima da Média**: Retorna clientes que possuem mais chamados de suporte do que a média geral
2. **Projetos com Tarefas de Alta Prioridade**: Lista projetos que contêm tarefas marcadas como alta prioridade

#### Funções de Grupo
1. **Resumo Financeiro por Projeto**: Análise completa usando SUM, COUNT e AVG para calcular receitas, despesas e saldo
2. **Estatísticas de Suporte**: Top 10 clientes com mais chamados usando COUNT, MAX e MIN

#### Operadores de Conjunto
1. **Contas Pendentes (UNION)**: Combina contas a pagar e receber pendentes em uma única listagem
2. **CPFs em Comum (INTERSECT)**: Identifica CPFs que aparecem tanto em leads quanto em clientes

## Estrutura do Projeto

```
wevo_media_bd/
├── actions/                    # Scripts originais de manipulação do BD
│   ├── create.py              # Criação de todas as tabelas
│   ├── insert.py              # Inserção de dados
│   ├── select.py              # Consultas SELECT
│   ├── update.py              # Atualização de dados
│   ├── delete.py              # Exclusão de dados
│   └── addons.py              # Consultas especiais
├── core/                      # App principal Django
│   ├── models.py              # Models de todas as tabelas
│   ├── views.py               # Views de autenticação e CRUD
│   ├── views_crud.py          # Views CRUD complementares
│   ├── views_queries.py       # Views de consultas especiais
│   ├── urls.py                # URLs da aplicação
│   ├── auth.py                # Sistema de autenticação
│   └── admin.py               # Configuração Django Admin
├── templates/                 # Templates HTML
│   ├── base.html              # Template base
│   ├── dashboard.html         # Dashboard principal
│   ├── auth/                  # Templates de autenticação
│   ├── leads/                 # Templates de leads
│   ├── clientes/              # Templates de clientes
│   ├── suporte/               # Templates de suporte
│   ├── projetos/              # Templates de projetos
│   ├── contratos/             # Templates de contratos
│   ├── financeiro/            # Templates financeiro
│   ├── tarefas/               # Templates de tarefas
│   ├── contas_pagar/          # Templates de contas a pagar
│   ├── contas_receber/        # Templates de contas a receber
│   ├── usuarios/              # Templates de usuários
│   └── queries/               # Templates de consultas
├── wevo_media_project/        # Configurações Django
│   ├── settings.py            # Configurações do projeto
│   ├── urls.py                # URLs principais
│   ├── wsgi.py                # WSGI
│   └── asgi.py                # ASGI
├── utils/                     # Utilitários
│   └── connection_db.py       # Conexão com PostgreSQL
├── manage.py                  # Script de gerenciamento Django
├── main.py                    # Script original de teste
├── requirements.txt           # Dependências Python
├── .env                       # Variáveis de ambiente
└── README.md                  # Esta documentação
```

## Uso do Sistema

### Dashboard
Após o login, você verá o dashboard com:
- Estatísticas gerais (total de leads, clientes, projetos e tarefas)
- Menu de acesso rápido para criar novos registros
- Informações do usuário logado

### Navegação
Use o menu lateral para acessar:
- **Gestão**: Leads, Clientes, Suporte, Projetos, Tarefas
- **Financeiro**: Contratos, Financeiro, Contas a Pagar, Contas a Receber
- **Relatórios**: Consultas Especiais
- **Administração** (apenas Admin): Usuários

### Consultas Especiais
Acesse o menu "Consultas Especiais" para visualizar os 6 relatórios SQL avançados que demonstram:
- SELECT aninhado (2 consultas)
- Funções de grupo (2 consultas)
- Operadores de conjunto (2 consultas)

## Desenvolvimento

### Boas Práticas Implementadas

1. **Separação de Responsabilidades**: Views divididas em módulos (views.py, views_crud.py, views_queries.py)
2. **Decoradores Customizados**: `@require_login` e `@require_admin` para controle de acesso
3. **Templates Modulares**: Template base reutilizável para todas as páginas
4. **Código DRY**: Gerador automático de templates CRUD (generate_templates.py)
5. **Models Desacoplados**: Uso de `managed=False` para trabalhar com tabelas existentes

### Gerador de Templates

O arquivo `generate_templates.py` pode ser usado para gerar automaticamente templates CRUD para novas entidades:

```bash
python generate_templates.py
```

## Requisitos do Trabalho Acadêmico

✅ **CRUD completo** para todas as tabelas, incluindo tabelas de relacionamento

✅ **Consulta com 3 tabelas**: Implementada em `views_queries.py` (Leads → Clientes → Suporte)

✅ **2 Consultas com SELECT aninhado**:
- Clientes com mais chamados que a média
- Projetos com tarefas de alta prioridade

✅ **2 Consultas com funções de grupo**:
- Resumo financeiro por projeto (SUM, COUNT, AVG)
- Estatísticas de suporte (COUNT, MAX, MIN)

✅ **2 Consultas com operadores de conjunto**:
- União de contas pendentes (UNION)
- CPFs em comum (INTERSECT)

✅ **Interface visual** com Django e Bootstrap 5

✅ **Sistema de login** com perfis Admin e Normal

✅ **Código modularizado** e seguindo boas práticas

## Autor

Desenvolvido como trabalho acadêmico de Banco de Dados - 2024

## Licença

Este projeto é um trabalho acadêmico e está disponível para fins educacionais.
