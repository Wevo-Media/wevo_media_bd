"""
Views para o sistema Wevo Media.
Incluindo autenticação, CRUD e consultas especiais.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db import connection
from django.db.models import Count, Sum, Avg, Q
from .models import (
    Lead, Cliente, Suporte, Usuario, Projeto, Contrato,
    Financeiro, Tarefa, ContaAPagar, ContaAReceber,
    ClienteContrato, UsuarioProjeto, UsuarioTarefa
)
from .auth import criar_usuario


# =============================================================================
# VIEWS DE AUTENTICAÇÃO
# =============================================================================

def login_view(request):
    """View de login"""
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(senha, usuario.senha):
                request.session['usuario_cpf'] = usuario.cpf
                request.session['usuario_nome'] = usuario.nome
                request.session['usuario_perfil'] = usuario.perfil
                request.session['usuario_email'] = usuario.email
                messages.success(request, f'Bem-vindo, {usuario.nome}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'E-mail ou senha incorretos.')
        except Usuario.DoesNotExist:
            messages.error(request, 'E-mail ou senha incorretos.')

    return render(request, 'auth/login.html')


def logout_view(request):
    """View de logout"""
    request.session.flush()
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('login')


def registro_view(request):
    """View de registro de novo usuário"""
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        if senha != confirma_senha:
            messages.error(request, 'As senhas não conferem.')
        elif Usuario.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já cadastrado.')
        elif Usuario.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
        else:
            criar_usuario(cpf, nome, email, senha, perfil='normal')
            messages.success(request, 'Usuário cadastrado com sucesso! Faça login.')
            return redirect('login')

    return render(request, 'auth/registro.html')


def require_login(view_func):
    """Decorator customizado para exigir login - PROTEÇÃO FORTE"""
    def wrapper(request, *args, **kwargs):
        # Verifica se o usuário está logado na sessão
        if 'usuario_cpf' not in request.session or 'usuario_email' not in request.session:
            messages.warning(request, 'Sua sessão expirou. Por favor, faça login novamente.')
            # Limpa qualquer resíduo de sessão
            request.session.flush()
            return redirect('login')

        # Verifica se o usuário ainda existe no banco
        try:
            Usuario.objects.get(cpf=request.session['usuario_cpf'])
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado. Por favor, faça login novamente.')
            request.session.flush()
            return redirect('login')

        return view_func(request, *args, **kwargs)
    return wrapper


def require_admin(view_func):
    """Decorator customizado para exigir perfil admin"""
    def wrapper(request, *args, **kwargs):
        if 'usuario_cpf' not in request.session:
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('login')
        if request.session.get('usuario_perfil') != 'admin':
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# =============================================================================
# DASHBOARD
# =============================================================================

@require_login
def dashboard_view(request):
    """Dashboard principal"""
    context = {
        'total_leads': Lead.objects.count(),
        'total_clientes': Cliente.objects.count(),
        'total_projetos': Projeto.objects.count(),
        'total_tarefas': Tarefa.objects.count(),
        'usuario_nome': request.session.get('usuario_nome'),
        'usuario_perfil': request.session.get('usuario_perfil'),
    }
    return render(request, 'dashboard.html', context)


# =============================================================================
# CRUD GENÉRICO - LEADS
# =============================================================================

@require_login
def lead_list(request):
    """Lista todos os leads"""
    leads = Lead.objects.all().order_by('-id_lead')
    return render(request, 'leads/list.html', {'leads': leads})


@require_login
def lead_create(request):
    """Cria um novo lead"""
    if request.method == 'POST':
        Lead.objects.create(
            nome=request.POST.get('nome'),
            telefone=request.POST.get('telefone'),
            email=request.POST.get('email'),
            origem=request.POST.get('origem'),
            status_funil=request.POST.get('status_funil'),
            cpf=request.POST.get('cpf')
        )
        messages.success(request, 'Lead cadastrado com sucesso!')
        return redirect('lead_list')
    return render(request, 'leads/form.html')


@require_login
def lead_update(request, pk):
    """Atualiza um lead"""
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        lead.nome = request.POST.get('nome')
        lead.telefone = request.POST.get('telefone')
        lead.email = request.POST.get('email')
        lead.origem = request.POST.get('origem')
        lead.status_funil = request.POST.get('status_funil')
        lead.cpf = request.POST.get('cpf')
        lead.save()
        messages.success(request, 'Lead atualizado com sucesso!')
        return redirect('lead_list')
    return render(request, 'leads/form.html', {'lead': lead})


@require_admin
def lead_delete(request, pk):
    """Deleta um lead (apenas admin)"""
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    messages.success(request, 'Lead deletado com sucesso!')
    return redirect('lead_list')


# =============================================================================
# CRUD GENÉRICO - CLIENTES
# =============================================================================

@require_login
def cliente_list(request):
    """Lista todos os clientes"""
    clientes = Cliente.objects.all().select_related('id_lead').order_by('-id_cliente')
    return render(request, 'clientes/list.html', {'clientes': clientes})


@require_login
def cliente_create(request):
    """Cria um novo cliente"""
    if request.method == 'POST':
        id_lead = request.POST.get('id_lead')
        Cliente.objects.create(
            nome=request.POST.get('nome'),
            telefone=request.POST.get('telefone'),
            email=request.POST.get('email'),
            cpf=request.POST.get('cpf'),
            plano_ativo=request.POST.get('plano_ativo') == 'on',
            id_lead_id=id_lead if id_lead else None
        )
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return redirect('cliente_list')
    leads = Lead.objects.all()
    return render(request, 'clientes/form.html', {'leads': leads})


@require_login
def cliente_update(request, pk):
    """Atualiza um cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        id_lead = request.POST.get('id_lead')
        cliente.nome = request.POST.get('nome')
        cliente.telefone = request.POST.get('telefone')
        cliente.email = request.POST.get('email')
        cliente.cpf = request.POST.get('cpf')
        cliente.plano_ativo = request.POST.get('plano_ativo') == 'on'
        cliente.id_lead_id = id_lead if id_lead else None
        cliente.save()
        messages.success(request, 'Cliente atualizado com sucesso!')
        return redirect('cliente_list')
    leads = Lead.objects.all()
    return render(request, 'clientes/form.html', {'cliente': cliente, 'leads': leads})


@require_admin
def cliente_delete(request, pk):
    """Deleta um cliente (apenas admin)"""
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    messages.success(request, 'Cliente deletado com sucesso!')
    return redirect('cliente_list')


# =============================================================================
# CRUD GENÉRICO - SUPORTE
# =============================================================================

@require_login
def suporte_list(request):
    """Lista todos os chamados de suporte"""
    chamados = Suporte.objects.all().select_related('id_cliente').order_by('-data_solicitacao')
    return render(request, 'suporte/list.html', {'chamados': chamados})


@require_login
def suporte_create(request):
    """Cria um novo chamado de suporte"""
    if request.method == 'POST':
        Suporte.objects.create(
            nome_pedido=request.POST.get('nome_pedido'),
            responsavel_solicitacao=request.POST.get('responsavel_solicitacao'),
            descricao=request.POST.get('descricao'),
            id_cliente_id=request.POST.get('id_cliente')
        )
        messages.success(request, 'Chamado cadastrado com sucesso!')
        return redirect('suporte_list')
    clientes = Cliente.objects.all()
    return render(request, 'suporte/form.html', {'clientes': clientes})


@require_login
def suporte_update(request, pk):
    """Atualiza um chamado de suporte"""
    chamado = get_object_or_404(Suporte, pk=pk)
    if request.method == 'POST':
        chamado.nome_pedido = request.POST.get('nome_pedido')
        chamado.responsavel_solicitacao = request.POST.get('responsavel_solicitacao')
        chamado.descricao = request.POST.get('descricao')
        chamado.id_cliente_id = request.POST.get('id_cliente')
        chamado.save()
        messages.success(request, 'Chamado atualizado com sucesso!')
        return redirect('suporte_list')
    clientes = Cliente.objects.all()
    return render(request, 'suporte/form.html', {'chamado': chamado, 'clientes': clientes})


@require_admin
def suporte_delete(request, pk):
    """Deleta um chamado de suporte (apenas admin)"""
    chamado = get_object_or_404(Suporte, pk=pk)
    chamado.delete()
    messages.success(request, 'Chamado deletado com sucesso!')
    return redirect('suporte_list')


# Continua na próxima parte...
