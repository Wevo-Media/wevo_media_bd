"""
Script para gerar templates CRUD automaticamente.
"""
import os

TEMPLATES_DIR = "templates"

# Definição das entidades e seus campos
ENTITIES = {
    "clientes": {
        "title": "Clientes",
        "icon": "person-check",
        "fields": [
            {"name": "nome", "label": "Nome", "type": "text", "required": True},
            {"name": "cpf", "label": "CPF", "type": "text", "required": False},
            {"name": "telefone", "label": "Telefone", "type": "text", "required": False},
            {"name": "email", "label": "E-mail", "type": "email", "required": False},
            {"name": "plano_ativo", "label": "Plano Ativo", "type": "checkbox", "required": False},
            {"name": "id_lead", "label": "Lead Origem", "type": "select", "foreign": "leads", "required": False},
        ],
        "list_columns": ["id_cliente", "nome", "email", "telefone", "plano_ativo"],
    },
    "suporte": {
        "title": "Suporte",
        "icon": "headset",
        "fields": [
            {"name": "nome_pedido", "label": "Nome do Pedido", "type": "text", "required": True},
            {"name": "responsavel_solicitacao", "label": "Responsável", "type": "text", "required": False},
            {"name": "descricao", "label": "Descrição", "type": "textarea", "required": False},
            {"name": "id_cliente", "label": "Cliente", "type": "select", "foreign": "clientes", "required": True},
        ],
        "list_columns": ["id_chamado", "nome_pedido", "responsavel_solicitacao", "id_cliente"],
    },
    "projetos": {
        "title": "Projetos",
        "icon": "kanban",
        "fields": [
            {"name": "nome_projeto", "label": "Nome do Projeto", "type": "text", "required": True},
            {"name": "descricao", "label": "Descrição", "type": "textarea", "required": False},
            {"name": "status", "label": "Status", "type": "select", "options": ["Em andamento", "Concluído", "Pausado"], "required": False},
        ],
        "list_columns": ["id_projeto", "nome_projeto", "status"],
    },
    "contratos": {
        "title": "Contratos",
        "icon": "file-earmark-text",
        "fields": [
            {"name": "data_inicio", "label": "Data Início", "type": "date", "required": True},
            {"name": "data_termino", "label": "Data Término", "type": "date", "required": False},
            {"name": "valor", "label": "Valor", "type": "number", "required": True},
            {"name": "status", "label": "Status", "type": "select", "options": ["Ativo", "Inativo", "Cancelado"], "required": False},
            {"name": "cpf_responsavel", "label": "Responsável", "type": "select", "foreign": "usuarios", "required": False},
        ],
        "list_columns": ["id_contrato", "data_inicio", "valor", "status"],
    },
    "financeiro": {
        "title": "Financeiro",
        "icon": "cash-stack",
        "fields": [
            {"name": "descricao", "label": "Descrição", "type": "text", "required": False},
            {"name": "valor", "label": "Valor", "type": "number", "required": True},
            {"name": "tipo", "label": "Tipo", "type": "select", "options": ["Receita", "Despesa"], "required": True},
            {"name": "id_projeto", "label": "Projeto", "type": "select", "foreign": "projetos", "required": False},
        ],
        "list_columns": ["id_financeiro", "descricao", "valor", "tipo"],
    },
    "tarefas": {
        "title": "Tarefas",
        "icon": "check2-square",
        "fields": [
            {"name": "responsavel", "label": "Responsável", "type": "text", "required": False},
            {"name": "status", "label": "Status", "type": "select", "options": ["Pendente", "Em Andamento", "Concluída"], "required": False},
            {"name": "prioridade", "label": "Prioridade", "type": "select", "options": ["Baixa", "Média", "Alta"], "required": False},
            {"name": "descricao", "label": "Descrição", "type": "textarea", "required": False},
            {"name": "id_projeto", "label": "Projeto", "type": "select", "foreign": "projetos", "required": False},
        ],
        "list_columns": ["id_tarefas", "responsavel", "status", "prioridade"],
    },
    "contas_pagar": {
        "title": "Contas a Pagar",
        "icon": "arrow-up-circle",
        "fields": [
            {"name": "home_beneficiada", "label": "Beneficiário", "type": "text", "required": False},
            {"name": "data_vencimento", "label": "Data Vencimento", "type": "date", "required": True},
            {"name": "valor", "label": "Valor", "type": "number", "required": True},
            {"name": "descricao", "label": "Descrição", "type": "textarea", "required": False},
            {"name": "status", "label": "Status", "type": "select", "options": ["Pendente", "Pago", "Atrasado"], "required": False},
        ],
        "list_columns": ["id_conta_pagar", "home_beneficiada", "data_vencimento", "valor", "status"],
    },
    "contas_receber": {
        "title": "Contas a Receber",
        "icon": "arrow-down-circle",
        "fields": [
            {"name": "data_recebimento", "label": "Data Recebimento", "type": "date", "required": False},
            {"name": "valor", "label": "Valor", "type": "number", "required": True},
            {"name": "descricao", "label": "Descrição", "type": "textarea", "required": False},
            {"name": "id_cliente", "label": "Cliente", "type": "select", "foreign": "clientes", "required": False},
            {"name": "status", "label": "Status", "type": "select", "options": ["Pendente", "Recebido", "Atrasado"], "required": False},
        ],
        "list_columns": ["id_conta_receber", "id_cliente", "data_recebimento", "valor", "status"],
    },
    "usuarios": {
        "title": "Usuários",
        "icon": "person-gear",
        "fields": [
            {"name": "cpf", "label": "CPF", "type": "text", "required": True},
            {"name": "nome", "label": "Nome", "type": "text", "required": True},
            {"name": "email", "label": "E-mail", "type": "email", "required": True},
            {"name": "senha", "label": "Senha", "type": "password", "required": True},
            {"name": "perfil", "label": "Perfil", "type": "select", "options": ["admin", "normal"], "required": False},
        ],
        "list_columns": ["cpf", "nome", "email", "perfil"],
    },
}


def generate_list_template(entity_name, config):
    """Gera template de listagem"""
    pk = "cpf" if entity_name == "usuarios" else f"id_{entity_name[:-1] if entity_name.endswith('s') else entity_name}"
    singular = entity_name.rstrip("s")

    template = f'''
{{% extends 'base.html' %}}

{{% block title %}}{config['title']} - Wevo Media{{% endblock %}}

{{% block page_title %}}Gerenciar {config['title']}{{% endblock %}}

{{% block content %}}
<div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0"><i class="bi bi-{config['icon']}"></i> Lista de {config['title']}</h5>
        <a href="{{% url '{singular}_create' %}}" class="btn btn-primary">
            <i class="bi bi-plus-circle"></i> Novo
        </a>
    </div>
    <div class="card-body">
        {{% if {entity_name} %}}
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        {" ".join([f"<th>{col.replace('_', ' ').title()}</th>" for col in config['list_columns']])}
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {{% for item in {entity_name} %}}
                    <tr>
                        {" ".join([f"<td>{{{{ item.{col}|default:'-' }}}}</td>" for col in config['list_columns']])}
                        <td>
                            <a href="{{% url '{singular}_update' item.{pk} %}}" class="btn btn-sm btn-outline-primary">
                                <i class="bi bi-pencil"></i>
                            </a>
                            {{% if request.session.usuario_perfil == 'admin' %}}
                            <a href="{{% url '{singular}_delete' item.{pk} %}}"
                               class="btn btn-sm btn-outline-danger"
                               onclick="return confirm('Tem certeza que deseja deletar?')">
                                <i class="bi bi-trash"></i>
                            </a>
                            {{% endif %}}
                        </td>
                    </tr>
                    {{% endfor %}}
                </tbody>
            </table>
        </div>
        {{% else %}}
        <div class="alert alert-info">
            <i class="bi bi-info-circle"></i> Nenhum registro cadastrado ainda.
        </div>
        {{% endif %}}
    </div>
</div>
{{% endblock %}}
'''
    return template.strip()


def generate_form_template(entity_name, config):
    """Gera template de formulário"""
    singular = entity_name.rstrip("s")
    item_var = "item" if entity_name == "usuarios" else singular

    form_fields = ""
    for field in config['fields']:
        if field['type'] == 'textarea':
            form_fields += f'''
                <div class="mb-3">
                    <label for="{field['name']}" class="form-label">{field['label']}</label>
                    <textarea class="form-control" id="{field['name']}" name="{field['name']}" rows="3"
                           {'required' if field['required'] else ''}></textarea>
                </div>
            '''
        elif field['type'] == 'checkbox':
            form_fields += f'''
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="{field['name']}" name="{field['name']}">
                    <label class="form-check-label" for="{field['name']}">{field['label']}</label>
                </div>
            '''
        elif field['type'] == 'select':
            if 'foreign' in field:
                form_fields += f'''
                <div class="mb-3">
                    <label for="{field['name']}" class="form-label">{field['label']}</label>
                    <select class="form-select" id="{field['name']}" name="{field['name']}" {'required' if field['required'] else ''}>
                        <option value="">Selecione...</option>
                    </select>
                </div>
            '''
            else:
                options = ''.join([f'<option value="{opt}">{opt}</option>' for opt in field.get('options', [])])
                form_fields += f'''
                <div class="mb-3">
                    <label for="{field['name']}" class="form-label">{field['label']}</label>
                    <select class="form-select" id="{field['name']}" name="{field['name']}" {'required' if field['required'] else ''}>
                        <option value="">Selecione...</option>
                        {options}
                    </select>
                </div>
            '''
        else:
            form_fields += f'''
                <div class="mb-3">
                    <label for="{field['name']}" class="form-label">{field['label']} {'*' if field['required'] else ''}</label>
                    <input type="{field['type']}" class="form-control" id="{field['name']}" name="{field['name']}"
                           value=""
                           {'required' if field['required'] else ''}>
                </div>
            '''

    template = f'''
{{% extends 'base.html' %}}

{{% block title %}}{{% if {item_var} %}}Editar{{% else %}}Novo{{% endif %}} - {config['title']}{{% endblock %}}

{{% block page_title %}}{{% if {item_var} %}}Editar{{% else %}}Novo{{% endif %}} {config['title']}{{% endblock %}}

{{% block content %}}
<div class="card">
    <div class="card-header">
        <h5 class="mb-0">
            <i class="bi bi-{config['icon']}"></i>
            {{% if {item_var} %}}Editar{{% else %}}Cadastrar{{% endif %}}
        </h5>
    </div>
    <div class="card-body">
        <form method="post">
            {{% csrf_token %}}
            {form_fields}
            <hr>
            <div class="d-flex justify-content-between">
                <a href="{{% url '{singular}_list' %}}" class="btn btn-secondary">
                    <i class="bi bi-arrow-left"></i> Voltar
                </a>
                <button type="submit" class="btn btn-primary">
                    <i class="bi bi-check-circle"></i> Salvar
                </button>
            </div>
        </form>
    </div>
</div>
{{% endblock %}}
'''
    return template.strip()


def main():
    """Gera todos os templates"""
    print("Gerando templates CRUD...")

    for entity_name, config in ENTITIES.items():
        print(f"\nGerando templates para: {entity_name}")

        # Criar pasta se não existir
        entity_dir = os.path.join(TEMPLATES_DIR, entity_name)
        os.makedirs(entity_dir, exist_ok=True)

        # Gerar template de listagem
        list_template = generate_list_template(entity_name, config)
        list_path = os.path.join(entity_dir, "list.html")
        with open(list_path, 'w', encoding='utf-8') as f:
            f.write(list_template)
        print(f"  [OK] Criado: {list_path}")

        # Gerar template de formulário
        form_template = generate_form_template(entity_name, config)
        form_path = os.path.join(entity_dir, "form.html")
        with open(form_path, 'w', encoding='utf-8') as f:
            f.write(form_template)
        print(f"  [OK] Criado: {form_path}")

    print("\n[OK] Templates gerados com sucesso!")


if __name__ == "__main__":
    main()
