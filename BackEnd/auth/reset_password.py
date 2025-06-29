# BackEnd/auth/reset_password.py
from .supabase_client import supabase

def reset_password(nickname: str):
    # Busca o e-mail correspondente ao nickname
    result = supabase.table("Pessoa").select("Email").eq("Nickname", nickname).single().execute()

    if not result.data:
        raise Exception("Nickname não encontrado")

    email = result.data["Email"]

    # Envia e-mail de redefinição de senha
    reset_response = supabase.auth.reset_password_email(email)

    if not reset_response:
        raise Exception("Erro ao solicitar redefinição de senha")

    return "E-mail de redefinição enviado com sucesso."
