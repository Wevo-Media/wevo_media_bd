"""
Registro dos models no Django Admin.
"""
from django.contrib import admin
from .models import (
    Lead, Cliente, Suporte, Usuario, Projeto, Contrato,
    Financeiro, Tarefa, ContaAPagar, ContaAReceber,
    ClienteContrato, UsuarioProjeto, UsuarioTarefa
)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id_lead', 'nome', 'email', 'telefone', 'origem', 'status_funil')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('origem', 'status_funil')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'nome', 'email', 'telefone', 'plano_ativo')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('plano_ativo',)


@admin.register(Suporte)
class SuporteAdmin(admin.ModelAdmin):
    list_display = ('id_chamado', 'nome_pedido', 'id_cliente', 'responsavel_solicitacao', 'data_solicitacao')
    search_fields = ('nome_pedido', 'descricao')
    list_filter = ('data_solicitacao',)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'nome', 'email', 'perfil')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('perfil',)


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('id_projeto', 'nome_projeto', 'status')
    search_fields = ('nome_projeto', 'descricao')
    list_filter = ('status',)


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id_contrato', 'data_inicio', 'data_termino', 'valor', 'status')
    search_fields = ('id_contrato',)
    list_filter = ('status', 'data_inicio')


@admin.register(Financeiro)
class FinanceiroAdmin(admin.ModelAdmin):
    list_display = ('id_financeiro', 'descricao', 'valor', 'tipo', 'data')
    search_fields = ('descricao',)
    list_filter = ('tipo', 'data')


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('id_tarefas', 'responsavel', 'status', 'prioridade')
    search_fields = ('responsavel', 'descricao')
    list_filter = ('status', 'prioridade')


@admin.register(ContaAPagar)
class ContaAPagarAdmin(admin.ModelAdmin):
    list_display = ('id_conta_pagar', 'home_beneficiada', 'data_vencimento', 'valor', 'status')
    search_fields = ('home_beneficiada', 'descricao')
    list_filter = ('status', 'data_vencimento')


@admin.register(ContaAReceber)
class ContaAReceberAdmin(admin.ModelAdmin):
    list_display = ('id_conta_receber', 'id_cliente', 'data_recebimento', 'valor', 'status')
    search_fields = ('descricao',)
    list_filter = ('status', 'data_recebimento')


@admin.register(ClienteContrato)
class ClienteContratoAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'id_contrato')


@admin.register(UsuarioProjeto)
class UsuarioProjetoAdmin(admin.ModelAdmin):
    list_display = ('cpf_usuario', 'id_projeto')


@admin.register(UsuarioTarefa)
class UsuarioTarefaAdmin(admin.ModelAdmin):
    list_display = ('cpf_usuario', 'id_tarefa')
