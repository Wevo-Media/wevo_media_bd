"""
Script de configuração inicial do sistema Wevo Media.
Cria o banco de dados, tabelas e usuário administrador padrão.
"""
import sys
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wevo_media_project.settings')
django.setup()

from utils.connection_db import ConnectionDB
from actions.create import CreateTables
from core.auth import criar_usuario
from core.models import Usuario


def criar_banco_e_tabelas():
    """Cria o banco de dados e todas as tabelas"""
    print("=" * 60)
    print("SETUP INICIAL - SISTEMA WEVO MEDIA")
    print("=" * 60)
    print()

    # Criar banco de dados
    print("[1/3] Criando banco de dados...")
    import psycopg2
    try:
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'wevo_media';")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("CREATE DATABASE wevo_media;")
            print("   -> Banco de dados 'wevo_media' criado com sucesso!")
        else:
            print("   -> Banco de dados 'wevo_media' ja existe.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"   -> Erro ao criar banco: {e}")
        return False

    # Executar migrations do Django
    print("\n[2/4] Executando migrations do Django...")
    try:
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        print("   -> Migrations do Django aplicadas com sucesso!")
    except Exception as e:
        print(f"   -> Erro ao executar migrations: {e}")
        return False

    # Criar tabelas personalizadas
    print("\n[3/4] Criando tabelas do sistema...")
    try:
        connection = ConnectionDB().create_connection()
        if connection:
            creator = CreateTables(connection)
            creator.execute()
            connection.close()
        else:
            print("   -> Erro: Nao foi possivel conectar ao banco de dados.")
            return False
    except Exception as e:
        print(f"   -> Erro ao criar tabelas: {e}")
        return False

    # Criar usuário admin
    print("\n[4/4] Criando usuario administrador...")
    try:
        # Verificar se já existe admin
        admin_exists = Usuario.objects.filter(cpf="00000000000").exists()

        if not admin_exists:
            criar_usuario(
                cpf="00000000000",
                nome="Administrador",
                email="admin@wevomedia.com",
                senha="admin123",
                perfil="admin"
            )
            print("   -> Usuario administrador criado!")
            print("      E-mail: admin@wevomedia.com")
            print("      Senha: admin123")
        else:
            print("   -> Usuario administrador ja existe.")
            print("      E-mail: admin@wevomedia.com")
    except Exception as e:
        print(f"   -> Erro ao criar usuario admin: {e}")
        return False

    return True


def main():
    """Função principal"""
    sucesso = criar_banco_e_tabelas()

    print()
    print("=" * 60)
    if sucesso:
        print("SETUP CONCLUIDO COM SUCESSO!")
        print()
        print("Proximo passo:")
        print("  1. Execute: python manage.py runserver")
        print("  2. Acesse: http://localhost:8000")
        print("  3. Faca login com:")
        print("     - E-mail: admin@wevomedia.com")
        print("     - Senha: admin123")
    else:
        print("SETUP CONCLUIDO COM ERROS!")
        print("Verifique as mensagens acima e tente novamente.")
    print("=" * 60)


if __name__ == "__main__":
    main()
