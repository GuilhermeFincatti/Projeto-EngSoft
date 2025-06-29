from .supabase_client import supabase

def login_user(nickname: str, password: str):
    # Busca o e-mail correspondente ao nickname
    result = supabase.table("pessoa").select("email").eq("nickname", nickname).single().execute()

    if not result.data:
        raise Exception("Nickname não encontrado")

    email = result.data["email"]

    # Faz login com email e senha
    session_response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if not session_response.session:
        raise Exception("Falha no login")

    return session_response
