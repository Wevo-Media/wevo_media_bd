"""
Models Django para o sistema Wevo Media.
Usando managed=False para usar as tabelas já criadas no PostgreSQL.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Lead(models.Model):
    """Model para tabela de Leads"""
    id_lead = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    origem = models.CharField(max_length=50, null=True, blank=True)
    status_funil = models.CharField(max_length=50, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'leads'

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    """Model para tabela de Clientes"""
    id_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    plano_ativo = models.BooleanField(default=False)
    id_lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_lead')

    class Meta:
        managed = False
        db_table = 'clientes'

    def __str__(self):
        return self.nome


class Suporte(models.Model):
    """Model para tabela de Suporte"""
    id_chamado = models.AutoField(primary_key=True)
    nome_pedido = models.CharField(max_length=100)
    responsavel_solicitacao = models.CharField(max_length=100, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'suporte'

    def __str__(self):
        return self.nome_pedido


class Usuario(models.Model):
    """Model para tabela de Usuários"""
    PERFIL_CHOICES = [
        ('admin', 'Administrador'),
        ('normal', 'Usuário Normal'),
    ]

    cpf = models.CharField(max_length=14, primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=255)
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default='normal')

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nome} ({self.perfil})"


class Projeto(models.Model):
    """Model para tabela de Projetos"""
    id_projeto = models.AutoField(primary_key=True)
    nome_projeto = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Em andamento')

    class Meta:
        managed = False
        db_table = 'projeto'

    def __str__(self):
        return self.nome_projeto


class Contrato(models.Model):
    """Model para tabela de Contratos"""
    id_contrato = models.AutoField(primary_key=True)
    data_inicio = models.DateField()
    data_termino = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Ativo')
    cpf_responsavel = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, db_column='cpf_responsavel')

    class Meta:
        managed = False
        db_table = 'contrato'

    def __str__(self):
        return f"Contrato #{self.id_contrato} - {self.status}"


class Financeiro(models.Model):
    """Model para tabela Financeiro"""
    TIPO_CHOICES = [
        ('Receita', 'Receita'),
        ('Despesa', 'Despesa'),
    ]

    id_financeiro = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=200, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    id_projeto = models.ForeignKey(Projeto, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_projeto')

    class Meta:
        managed = False
        db_table = 'financeiro'

    def __str__(self):
        return f"{self.tipo} - R$ {self.valor}"


class Tarefa(models.Model):
    """Model para tabela de Tarefas"""
    PRIORIDADE_CHOICES = [
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
    ]

    id_tarefas = models.AutoField(primary_key=True)
    responsavel = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, default='Pendente')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    id_projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, null=True, blank=True, db_column='id_projeto')

    class Meta:
        managed = False
        db_table = 'tarefas'

    def __str__(self):
        return f"Tarefa #{self.id_tarefas} - {self.status}"


class ContaAPagar(models.Model):
    """Model para tabela Conta a Pagar"""
    id_conta_pagar = models.AutoField(primary_key=True)
    home_beneficiada = models.CharField(max_length=100, null=True, blank=True)
    data_vencimento = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Pendente')

    class Meta:
        managed = False
        db_table = 'conta_a_pagar'

    def __str__(self):
        return f"Conta a Pagar #{self.id_conta_pagar} - {self.status}"


class ContaAReceber(models.Model):
    """Model para tabela Conta a Receber"""
    id_conta_receber = models.AutoField(primary_key=True)
    data_recebimento = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(null=True, blank=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_cliente')
    status = models.CharField(max_length=50, default='Pendente')

    class Meta:
        managed = False
        db_table = 'conta_a_receber'

    def __str__(self):
        return f"Conta a Receber #{self.id_conta_receber} - {self.status}"


# Tabelas de Relacionamento N:N

class ClienteContrato(models.Model):
    """Relacionamento N:N entre Cliente e Contrato"""
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, db_column='id_contrato')

    class Meta:
        managed = False
        db_table = 'cliente_contrato'
        unique_together = (('id_cliente', 'id_contrato'),)

    def __str__(self):
        return f"Cliente {self.id_cliente} - Contrato {self.id_contrato}"


class UsuarioProjeto(models.Model):
    """Relacionamento N:N entre Usuario e Projeto (PARTICIPA)"""
    cpf_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cpf_usuario')
    id_projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, db_column='id_projeto')

    class Meta:
        managed = False
        db_table = 'usuario_projeto'
        unique_together = (('cpf_usuario', 'id_projeto'),)

    def __str__(self):
        return f"Usuario {self.cpf_usuario} - Projeto {self.id_projeto}"


class UsuarioTarefa(models.Model):
    """Relacionamento N:N entre Usuario e Tarefa (ATOCA)"""
    cpf_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='cpf_usuario')
    id_tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, db_column='id_tarefa')

    class Meta:
        managed = False
        db_table = 'usuario_tarefa'
        unique_together = (('cpf_usuario', 'id_tarefa'),)

    def __str__(self):
        return f"Usuario {self.cpf_usuario} - Tarefa {self.id_tarefa}"
