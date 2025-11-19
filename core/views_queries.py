"""
Views com consultas especiais para o trabalho acadêmico.
Incluindo: SELECT aninhado, funções de grupo e operadores de conjunto.
"""
from django.shortcuts import render
from django.db import connection
from .views import require_login


# =============================================================================
# CONSULTAS COM SELECT ANINHADO (2 consultas)
# =============================================================================

@require_login
def query_clientes_com_mais_chamados(request):
    """
    CONSULTA 1 - SELECT ANINHADO:
    Busca clientes que têm mais chamados de suporte do que a média.
    """
    query = """
        SELECT c.id_cliente, c.nome, c.email, COUNT(s.id_chamado) as total_chamados
        FROM clientes c
        LEFT JOIN suporte s ON c.id_cliente = s.id_cliente
        GROUP BY c.id_cliente, c.nome, c.email
        HAVING COUNT(s.id_chamado) > (
            SELECT AVG(chamados_por_cliente)
            FROM (
                SELECT COUNT(*) as chamados_por_cliente
                FROM suporte
                GROUP BY id_cliente
            ) AS subconsulta
        )
        ORDER BY total_chamados DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'title': 'Clientes com Chamados Acima da Média',
        'description': 'Clientes que possuem mais chamados de suporte do que a média',
        'results': results
    }
    return render(request, 'queries/results.html', context)


@require_login
def query_projetos_com_tarefas_alta_prioridade(request):
    """
    CONSULTA 2 - SELECT ANINHADO:
    Busca projetos que possuem tarefas de alta prioridade.
    """
    query = """
        SELECT p.id_projeto, p.nome_projeto, p.status,
               (SELECT COUNT(*)
                FROM tarefas t
                WHERE t.id_projeto = p.id_projeto
                  AND t.prioridade = 'Alta') as tarefas_alta_prioridade
        FROM projeto p
        WHERE EXISTS (
            SELECT 1
            FROM tarefas t
            WHERE t.id_projeto = p.id_projeto
              AND t.prioridade = 'Alta'
        )
        ORDER BY tarefas_alta_prioridade DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'title': 'Projetos com Tarefas de Alta Prioridade',
        'description': 'Projetos que possuem tarefas marcadas com prioridade alta',
        'results': results
    }
    return render(request, 'queries/results.html', context)


# =============================================================================
# CONSULTAS COM FUNÇÕES DE GRUPO (2 consultas)
# =============================================================================

@require_login
def query_resumo_financeiro_projetos(request):
    """
    CONSULTA 3 - FUNÇÕES DE GRUPO:
    Resumo financeiro por projeto com SUM, COUNT e AVG.
    """
    query = """
        SELECT
            p.id_projeto,
            p.nome_projeto,
            COUNT(f.id_financeiro) as total_registros,
            SUM(CASE WHEN f.tipo = 'Receita' THEN f.valor ELSE 0 END) as total_receitas,
            SUM(CASE WHEN f.tipo = 'Despesa' THEN f.valor ELSE 0 END) as total_despesas,
            SUM(CASE WHEN f.tipo = 'Receita' THEN f.valor ELSE -f.valor END) as saldo,
            AVG(f.valor) as media_valor
        FROM projeto p
        LEFT JOIN financeiro f ON p.id_projeto = f.id_projeto
        GROUP BY p.id_projeto, p.nome_projeto
        HAVING COUNT(f.id_financeiro) > 0
        ORDER BY saldo DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'title': 'Resumo Financeiro por Projeto',
        'description': 'Análise completa das receitas, despesas e saldo de cada projeto',
        'results': results
    }
    return render(request, 'queries/results.html', context)


@require_login
def query_estatisticas_suporte_cliente(request):
    """
    CONSULTA 4 - FUNÇÕES DE GRUPO:
    Estatísticas de chamados de suporte por cliente.
    """
    query = """
        SELECT
            c.id_cliente,
            c.nome,
            c.email,
            COUNT(s.id_chamado) as total_chamados,
            MAX(s.data_solicitacao) as ultimo_chamado,
            MIN(s.data_solicitacao) as primeiro_chamado
        FROM clientes c
        LEFT JOIN suporte s ON c.id_cliente = s.id_cliente
        GROUP BY c.id_cliente, c.nome, c.email
        ORDER BY total_chamados DESC
        LIMIT 10;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'title': 'Estatísticas de Suporte por Cliente',
        'description': 'Top 10 clientes com mais chamados de suporte e suas estatísticas',
        'results': results
    }
    return render(request, 'queries/results.html', context)


# =============================================================================
# CONSULTAS COM OPERADORES DE CONJUNTO (2 consultas)
# =============================================================================

@require_login
def query_uniao_contas_pendentes(request):
    """
    CONSULTA 5 - OPERADORES DE CONJUNTO (UNION):
    União de contas a pagar e receber pendentes.
    """
    query = """
        SELECT
            'A Pagar' as tipo_conta,
            id_conta_pagar as id_conta,
            descricao,
            valor,
            data_vencimento as data,
            status
        FROM conta_a_pagar
        WHERE status = 'Pendente'

        UNION ALL

        SELECT
            'A Receber' as tipo_conta,
            id_conta_receber as id_conta,
            descricao,
            valor,
            data_recebimento as data,
            status
        FROM conta_a_receber
        WHERE status = 'Pendente'

        ORDER BY data;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'title': 'Contas Pendentes - União',
        'description': 'Todas as contas a pagar e receber com status pendente (UNION)',
        'results': results
    }
    return render(request, 'queries/results.html', context)


@require_login
def query_clientes_leads_comum(request):
    """
    CONSULTA 6 - OPERADORES DE CONJUNTO (INTERSECT):
    CPFs que aparecem tanto em leads quanto em clientes.
    """
    query = """
        SELECT cpf, 'Lead e Cliente' as tipo
        FROM leads
        WHERE cpf IS NOT NULL

        INTERSECT

        SELECT cpf, 'Lead e Cliente' as tipo
        FROM clientes
        WHERE cpf IS NOT NULL

        ORDER BY cpf;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {
        'title': 'CPFs em Comum - Intersecção',
        'description': 'CPFs que aparecem tanto na tabela de leads quanto de clientes (INTERSECT)',
        'results': results
    }
    return render(request, 'queries/results.html', context)


# =============================================================================
# VIEW DE MENU DE CONSULTAS
# =============================================================================

@require_login
def queries_menu(request):
    """Menu principal de consultas especiais"""
    consultas = [
        {
            'url': 'query_clientes_chamados',
            'titulo': 'Clientes com Chamados Acima da Média',
            'tipo': 'SELECT Aninhado',
            'descricao': 'Clientes que possuem mais chamados de suporte do que a média'
        },
        {
            'url': 'query_projetos_alta_prioridade',
            'titulo': 'Projetos com Tarefas de Alta Prioridade',
            'tipo': 'SELECT Aninhado',
            'descricao': 'Projetos que possuem tarefas marcadas como alta prioridade'
        },
        {
            'url': 'query_resumo_financeiro',
            'titulo': 'Resumo Financeiro por Projeto',
            'tipo': 'Funções de Grupo',
            'descricao': 'Análise completa de receitas, despesas e saldo usando SUM, COUNT e AVG'
        },
        {
            'url': 'query_estatisticas_suporte',
            'titulo': 'Estatísticas de Suporte',
            'tipo': 'Funções de Grupo',
            'descricao': 'Top 10 clientes com mais chamados usando COUNT, MAX e MIN'
        },
        {
            'url': 'query_contas_pendentes',
            'titulo': 'Contas Pendentes - União',
            'tipo': 'Operador de Conjunto (UNION)',
            'descricao': 'Todas as contas a pagar e receber pendentes em uma única lista'
        },
        {
            'url': 'query_cpfs_comum',
            'titulo': 'CPFs em Comum - Intersecção',
            'tipo': 'Operador de Conjunto (INTERSECT)',
            'descricao': 'CPFs que aparecem tanto em leads quanto em clientes'
        },
    ]

    context = {'consultas': consultas}
    return render(request, 'queries/menu.html', context)
