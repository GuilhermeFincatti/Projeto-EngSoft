from .supabase_client import supabase

def register_user(nickname: str, email: str, password: str, tipo: str = "usuario"):
    print("→ Inserindo na tabela Pessoa")

    insert_data = {
        "nickname": nickname,
        "email": email,
        "tipo": tipo
    }

    pessoa_response = supabase.table("pessoa").insert(insert_data).execute()

    print("→ Resultado pessoa_response:", pessoa_response)

    if hasattr(pessoa_response, "error") and pessoa_response.error:
        print("→ Erro detalhado:", pessoa_response.error)
        raise Exception(f"Erro ao inserir na tabela Pessoa")

    print("→ Criando usuário no Supabase Auth")

    auth_response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    print("→ Resultado auth_response:", auth_response)

    if not auth_response.user:
        raise Exception("Erro ao criar usuário no Supabase Auth")

    return pessoa_response.data