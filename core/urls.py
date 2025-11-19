"""
URLs para o sistema Wevo Media.
"""
from django.urls import path
from . import views, views_crud, views_queries

urlpatterns = [
    # Autenticação
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # CRUD - Leads
    path('leads/', views.lead_list, name='lead_list'),
    path('leads/novo/', views.lead_create, name='lead_create'),
    path('leads/<int:pk>/editar/', views.lead_update, name='lead_update'),
    path('leads/<int:pk>/deletar/', views.lead_delete, name='lead_delete'),

    # CRUD - Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<int:pk>/deletar/', views.cliente_delete, name='cliente_delete'),

    # CRUD - Suporte
    path('suporte/', views.suporte_list, name='suporte_list'),
    path('suporte/novo/', views.suporte_create, name='suporte_create'),
    path('suporte/<int:pk>/editar/', views.suporte_update, name='suporte_update'),
    path('suporte/<int:pk>/deletar/', views.suporte_delete, name='suporte_delete'),

    # CRUD - Projetos
    path('projetos/', views_crud.projeto_list, name='projeto_list'),
    path('projetos/novo/', views_crud.projeto_create, name='projeto_create'),
    path('projetos/<int:pk>/editar/', views_crud.projeto_update, name='projeto_update'),
    path('projetos/<int:pk>/deletar/', views_crud.projeto_delete, name='projeto_delete'),

    # CRUD - Contratos
    path('contratos/', views_crud.contrato_list, name='contrato_list'),
    path('contratos/novo/', views_crud.contrato_create, name='contrato_create'),
    path('contratos/<int:pk>/editar/', views_crud.contrato_update, name='contrato_update'),
    path('contratos/<int:pk>/deletar/', views_crud.contrato_delete, name='contrato_delete'),

    # CRUD - Financeiro
    path('financeiro/', views_crud.financeiro_list, name='financeiro_list'),
    path('financeiro/novo/', views_crud.financeiro_create, name='financeiro_create'),
    path('financeiro/<int:pk>/editar/', views_crud.financeiro_update, name='financeiro_update'),
    path('financeiro/<int:pk>/deletar/', views_crud.financeiro_delete, name='financeiro_delete'),

    # CRUD - Tarefas
    path('tarefas/', views_crud.tarefa_list, name='tarefa_list'),
    path('tarefas/nova/', views_crud.tarefa_create, name='tarefa_create'),
    path('tarefas/<int:pk>/editar/', views_crud.tarefa_update, name='tarefa_update'),
    path('tarefas/<int:pk>/deletar/', views_crud.tarefa_delete, name='tarefa_delete'),

    # CRUD - Contas a Pagar
    path('contas-pagar/', views_crud.conta_pagar_list, name='conta_pagar_list'),
    path('contas-pagar/nova/', views_crud.conta_pagar_create, name='conta_pagar_create'),
    path('contas-pagar/<int:pk>/editar/', views_crud.conta_pagar_update, name='conta_pagar_update'),
    path('contas-pagar/<int:pk>/deletar/', views_crud.conta_pagar_delete, name='conta_pagar_delete'),

    # CRUD - Contas a Receber
    path('contas-receber/', views_crud.conta_receber_list, name='conta_receber_list'),
    path('contas-receber/nova/', views_crud.conta_receber_create, name='conta_receber_create'),
    path('contas-receber/<int:pk>/editar/', views_crud.conta_receber_update, name='conta_receber_update'),
    path('contas-receber/<int:pk>/deletar/', views_crud.conta_receber_delete, name='conta_receber_delete'),

    # CRUD - Usuários (apenas admin)
    path('usuarios/', views_crud.usuario_list, name='usuario_list'),
    path('usuarios/novo/', views_crud.usuario_create, name='usuario_create'),
    path('usuarios/<str:pk>/editar/', views_crud.usuario_update, name='usuario_update'),
    path('usuarios/<str:pk>/deletar/', views_crud.usuario_delete, name='usuario_delete'),
    path('usuarios/<str:pk>/toggle-admin/', views_crud.usuario_toggle_admin, name='usuario_toggle_admin'),

    # Consultas Especiais
    path('consultas/', views_queries.queries_menu, name='queries_menu'),
    path('consultas/clientes-chamados/', views_queries.query_clientes_com_mais_chamados, name='query_clientes_chamados'),
    path('consultas/projetos-alta-prioridade/', views_queries.query_projetos_com_tarefas_alta_prioridade, name='query_projetos_alta_prioridade'),
    path('consultas/resumo-financeiro/', views_queries.query_resumo_financeiro_projetos, name='query_resumo_financeiro'),
    path('consultas/estatisticas-suporte/', views_queries.query_estatisticas_suporte_cliente, name='query_estatisticas_suporte'),
    path('consultas/contas-pendentes/', views_queries.query_uniao_contas_pendentes, name='query_contas_pendentes'),
    path('consultas/cpfs-comum/', views_queries.query_clientes_leads_comum, name='query_cpfs_comum'),
]
