"""
Sistema de autenticação customizado usando a tabela Usuario.
"""
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password, make_password
from .models import Usuario


class UsuarioAuthBackend(BaseBackend):
    """
    Backend de autenticação customizado para a tabela Usuario.
    """

    def authenticate(self, request, email=None, password=None):
        """
        Autentica um usuário baseado no EMAIL e senha.
        """
        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(password, usuario.senha):
                return usuario
        except Usuario.DoesNotExist:
            return None
        return None

    def get_user(self, cpf):
        """
        Recupera um usuário pelo CPF.
        """
        try:
            return Usuario.objects.get(pk=cpf)
        except Usuario.DoesNotExist:
            return None


def criar_usuario(cpf, nome, email, senha, perfil='normal'):
    """
    Função helper para criar um novo usuário com senha hasheada.
    """
    usuario = Usuario(
        cpf=cpf,
        nome=nome,
        email=email,
        senha=make_password(senha),
        perfil=perfil
    )
    usuario.save()
    return usuario
