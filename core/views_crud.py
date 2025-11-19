"""
Views CRUD para as demais tabelas do sistema.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .views import require_login, require_admin
from .models import (
    Projeto, Contrato, Financeiro, Tarefa, ContaAPagar,
    ContaAReceber, Usuario, ClienteContrato, UsuarioProjeto, UsuarioTarefa
)


# =============================================================================
# CRUD - PROJETOS
# =============================================================================

@require_login
def projeto_list(request):
    """Lista todos os projetos"""
    projetos = Projeto.objects.all().order_by('-id_projeto')
    return render(request, 'projetos/list.html', {'projetos': projetos})


@require_login
def projeto_create(request):
    """Cria um novo projeto"""
    if request.method == 'POST':
        Projeto.objects.create(
            nome_projeto=request.POST.get('nome_projeto'),
            descricao=request.POST.get('descricao'),
            status=request.POST.get('status')
        )
        messages.success(request, 'Projeto cadastrado com sucesso!')
        return redirect('projeto_list')
    return render(request, 'projetos/form.html')


@require_login
def projeto_update(request, pk):
    """Atualiza um projeto"""
    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        projeto.nome_projeto = request.POST.get('nome_projeto')
        projeto.descricao = request.POST.get('descricao')
        projeto.status = request.POST.get('status')
        projeto.save()
        messages.success(request, 'Projeto atualizado com sucesso!')
        return redirect('projeto_list')
    return render(request, 'projetos/form.html', {'projeto': projeto})


@require_admin
def projeto_delete(request, pk):
    """Deleta um projeto"""
    projeto = get_object_or_404(Projeto, pk=pk)
    projeto.delete()
    messages.success(request, 'Projeto deletado com sucesso!')
    return redirect('projeto_list')


# =============================================================================
# CRUD - CONTRATOS
# =============================================================================

@require_login
def contrato_list(request):
    """Lista todos os contratos"""
    contratos = Contrato.objects.all().select_related('cpf_responsavel').order_by('-id_contrato')
    return render(request, 'contratos/list.html', {'contratos': contratos})


@require_login
def contrato_create(request):
    """Cria um novo contrato"""
    if request.method == 'POST':
        cpf_resp = request.POST.get('cpf_responsavel')
        Contrato.objects.create(
            data_inicio=request.POST.get('data_inicio'),
            data_termino=request.POST.get('data_termino') or None,
            valor=request.POST.get('valor'),
            status=request.POST.get('status'),
            cpf_responsavel_id=cpf_resp if cpf_resp else None
        )
        messages.success(request, 'Contrato cadastrado com sucesso!')
        return redirect('contrato_list')
    usuarios = Usuario.objects.all()
    return render(request, 'contratos/form.html', {'usuarios': usuarios})


@require_login
def contrato_update(request, pk):
    """Atualiza um contrato"""
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        cpf_resp = request.POST.get('cpf_responsavel')
        contrato.data_inicio = request.POST.get('data_inicio')
        contrato.data_termino = request.POST.get('data_termino') or None
        contrato.valor = request.POST.get('valor')
        contrato.status = request.POST.get('status')
        contrato.cpf_responsavel_id = cpf_resp if cpf_resp else None
        contrato.save()
        messages.success(request, 'Contrato atualizado com sucesso!')
        return redirect('contrato_list')
    usuarios = Usuario.objects.all()
    return render(request, 'contratos/form.html', {'contrato': contrato, 'usuarios': usuarios})


@require_admin
def contrato_delete(request, pk):
    """Deleta um contrato"""
    contrato = get_object_or_404(Contrato, pk=pk)
    contrato.delete()
    messages.success(request, 'Contrato deletado com sucesso!')
    return redirect('contrato_list')


# =============================================================================
# CRUD - FINANCEIRO
# =============================================================================

@require_login
def financeiro_list(request):
    """Lista todos os registros financeiros"""
    financeiros = Financeiro.objects.all().select_related('id_projeto').order_by('-data')
    return render(request, 'financeiro/list.html', {'financeiros': financeiros})


@require_login
def financeiro_create(request):
    """Cria um novo registro financeiro"""
    if request.method == 'POST':
        id_proj = request.POST.get('id_projeto')
        Financeiro.objects.create(
            descricao=request.POST.get('descricao'),
            valor=request.POST.get('valor'),
            tipo=request.POST.get('tipo'),
            id_projeto_id=id_proj if id_proj else None
        )
        messages.success(request, 'Registro financeiro cadastrado com sucesso!')
        return redirect('financeiro_list')
    projetos = Projeto.objects.all()
    return render(request, 'financeiro/form.html', {'projetos': projetos})


@require_login
def financeiro_update(request, pk):
    """Atualiza um registro financeiro"""
    financeiro = get_object_or_404(Financeiro, pk=pk)
    if request.method == 'POST':
        id_proj = request.POST.get('id_projeto')
        financeiro.descricao = request.POST.get('descricao')
        financeiro.valor = request.POST.get('valor')
        financeiro.tipo = request.POST.get('tipo')
        financeiro.id_projeto_id = id_proj if id_proj else None
        financeiro.save()
        messages.success(request, 'Registro financeiro atualizado com sucesso!')
        return redirect('financeiro_list')
    projetos = Projeto.objects.all()
    return render(request, 'financeiro/form.html', {'financeiro': financeiro, 'projetos': projetos})


@require_admin
def financeiro_delete(request, pk):
    """Deleta um registro financeiro"""
    financeiro = get_object_or_404(Financeiro, pk=pk)
    financeiro.delete()
    messages.success(request, 'Registro financeiro deletado com sucesso!')
    return redirect('financeiro_list')


# =============================================================================
# CRUD - TAREFAS
# =============================================================================

@require_login
def tarefa_list(request):
    """Lista todas as tarefas"""
    tarefas = Tarefa.objects.all().select_related('id_projeto').order_by('-id_tarefas')
    return render(request, 'tarefas/list.html', {'tarefas': tarefas})


@require_login
def tarefa_create(request):
    """Cria uma nova tarefa"""
    if request.method == 'POST':
        id_proj = request.POST.get('id_projeto')
        Tarefa.objects.create(
            responsavel=request.POST.get('responsavel'),
            status=request.POST.get('status'),
            prioridade=request.POST.get('prioridade'),
            descricao=request.POST.get('descricao'),
            id_projeto_id=id_proj if id_proj else None
        )
        messages.success(request, 'Tarefa cadastrada com sucesso!')
        return redirect('tarefa_list')
    projetos = Projeto.objects.all()
    return render(request, 'tarefas/form.html', {'projetos': projetos})


@require_login
def tarefa_update(request, pk):
    """Atualiza uma tarefa"""
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == 'POST':
        id_proj = request.POST.get('id_projeto')
        tarefa.responsavel = request.POST.get('responsavel')
        tarefa.status = request.POST.get('status')
        tarefa.prioridade = request.POST.get('prioridade')
        tarefa.descricao = request.POST.get('descricao')
        tarefa.id_projeto_id = id_proj if id_proj else None
        tarefa.save()
        messages.success(request, 'Tarefa atualizada com sucesso!')
        return redirect('tarefa_list')
    projetos = Projeto.objects.all()
    return render(request, 'tarefas/form.html', {'tarefa': tarefa, 'projetos': projetos})


@require_admin
def tarefa_delete(request, pk):
    """Deleta uma tarefa"""
    tarefa = get_object_or_404(Tarefa, pk=pk)
    tarefa.delete()
    messages.success(request, 'Tarefa deletada com sucesso!')
    return redirect('tarefa_list')


# =============================================================================
# CRUD - CONTA A PAGAR
# =============================================================================

@require_login
def conta_pagar_list(request):
    """Lista todas as contas a pagar"""
    contas = ContaAPagar.objects.all().order_by('-data_vencimento')
    return render(request, 'contas_pagar/list.html', {'contas': contas})


@require_login
def conta_pagar_create(request):
    """Cria uma nova conta a pagar"""
    if request.method == 'POST':
        ContaAPagar.objects.create(
            home_beneficiada=request.POST.get('home_beneficiada'),
            data_vencimento=request.POST.get('data_vencimento'),
            valor=request.POST.get('valor'),
            descricao=request.POST.get('descricao'),
            status=request.POST.get('status')
        )
        messages.success(request, 'Conta a pagar cadastrada com sucesso!')
        return redirect('conta_pagar_list')
    return render(request, 'contas_pagar/form.html')


@require_login
def conta_pagar_update(request, pk):
    """Atualiza uma conta a pagar"""
    conta = get_object_or_404(ContaAPagar, pk=pk)
    if request.method == 'POST':
        conta.home_beneficiada = request.POST.get('home_beneficiada')
        conta.data_vencimento = request.POST.get('data_vencimento')
        conta.valor = request.POST.get('valor')
        conta.descricao = request.POST.get('descricao')
        conta.status = request.POST.get('status')
        conta.save()
        messages.success(request, 'Conta a pagar atualizada com sucesso!')
        return redirect('conta_pagar_list')
    return render(request, 'contas_pagar/form.html', {'conta': conta})


@require_admin
def conta_pagar_delete(request, pk):
    """Deleta uma conta a pagar"""
    conta = get_object_or_404(ContaAPagar, pk=pk)
    conta.delete()
    messages.success(request, 'Conta a pagar deletada com sucesso!')
    return redirect('conta_pagar_list')


# =============================================================================
# CRUD - CONTA A RECEBER
# =============================================================================

@require_login
def conta_receber_list(request):
    """Lista todas as contas a receber"""
    contas = ContaAReceber.objects.all().select_related('id_cliente').order_by('-data_recebimento')
    return render(request, 'contas_receber/list.html', {'contas': contas})


@require_login
def conta_receber_create(request):
    """Cria uma nova conta a receber"""
    if request.method == 'POST':
        id_cli = request.POST.get('id_cliente')
        ContaAReceber.objects.create(
            data_recebimento=request.POST.get('data_recebimento') or None,
            valor=request.POST.get('valor'),
            descricao=request.POST.get('descricao'),
            id_cliente_id=id_cli if id_cli else None,
            status=request.POST.get('status')
        )
        messages.success(request, 'Conta a receber cadastrada com sucesso!')
        return redirect('conta_receber_list')
    clientes = Cliente.objects.all()
    from .models import Cliente
    return render(request, 'contas_receber/form.html', {'clientes': clientes})


@require_login
def conta_receber_update(request, pk):
    """Atualiza uma conta a receber"""
    conta = get_object_or_404(ContaAReceber, pk=pk)
    if request.method == 'POST':
        id_cli = request.POST.get('id_cliente')
        conta.data_recebimento = request.POST.get('data_recebimento') or None
        conta.valor = request.POST.get('valor')
        conta.descricao = request.POST.get('descricao')
        conta.id_cliente_id = id_cli if id_cli else None
        conta.status = request.POST.get('status')
        conta.save()
        messages.success(request, 'Conta a receber atualizada com sucesso!')
        return redirect('conta_receber_list')
    from .models import Cliente
    clientes = Cliente.objects.all()
    return render(request, 'contas_receber/form.html', {'conta': conta, 'clientes': clientes})


@require_admin
def conta_receber_delete(request, pk):
    """Deleta uma conta a receber"""
    conta = get_object_or_404(ContaAReceber, pk=pk)
    conta.delete()
    messages.success(request, 'Conta a receber deletada com sucesso!')
    return redirect('conta_receber_list')


# =============================================================================
# CRUD - USUÁRIOS (apenas admin)
# =============================================================================

@require_admin
def usuario_list(request):
    """Lista todos os usuários (apenas admin)"""
    usuarios = Usuario.objects.all().order_by('nome')
    return render(request, 'usuarios/list.html', {'usuarios': usuarios})


@require_admin
def usuario_create(request):
    """Cria um novo usuário (apenas admin)"""
    from .auth import criar_usuario
    if request.method == 'POST':
        criar_usuario(
            cpf=request.POST.get('cpf'),
            nome=request.POST.get('nome'),
            email=request.POST.get('email'),
            senha=request.POST.get('senha'),
            perfil=request.POST.get('perfil')
        )
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('usuario_list')
    return render(request, 'usuarios/form.html')


@require_admin
def usuario_update(request, pk):
    """Atualiza um usuário (apenas admin)"""
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.nome = request.POST.get('nome')
        usuario.email = request.POST.get('email')
        usuario.perfil = request.POST.get('perfil')

        nova_senha = request.POST.get('senha')
        if nova_senha:
            from django.contrib.auth.hashers import make_password
            usuario.senha = make_password(nova_senha)

        usuario.save()
        messages.success(request, 'Usuário atualizado com sucesso!')
        return redirect('usuario_list')
    return render(request, 'usuarios/form.html', {'usuario': usuario})


@require_admin
def usuario_delete(request, pk):
    """Deleta um usuário (apenas admin)"""
    usuario = get_object_or_404(Usuario, pk=pk)

    # Não permitir deletar a si mesmo
    if usuario.cpf == request.session.get('usuario_cpf'):
        messages.error(request, 'Você não pode deletar sua própria conta!')
        return redirect('usuario_list')

    usuario.delete()
    messages.success(request, 'Usuário deletado com sucesso!')
    return redirect('usuario_list')


@require_admin
def usuario_toggle_admin(request, pk):
    """Alterna o perfil de um usuário entre admin e normal (apenas admin)"""
    usuario = get_object_or_404(Usuario, pk=pk)

    # Não permitir alterar o próprio perfil
    if usuario.cpf == request.session.get('usuario_cpf'):
        messages.error(request, 'Você não pode alterar seu próprio perfil!')
        return redirect('usuario_list')

    # Alternar perfil
    if usuario.perfil == 'admin':
        usuario.perfil = 'normal'
        messages.success(request, f'{usuario.nome} agora é um usuário normal.')
    else:
        usuario.perfil = 'admin'
        messages.success(request, f'{usuario.nome} agora é um administrador!')

    usuario.save()
    return redirect('usuario_list')
