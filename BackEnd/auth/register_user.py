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

    # Se o tipo for "usuario", criar registro na tabela usuario
    if tipo.lower() == "usuario":
        print("→ Inserindo na tabela Usuario")
        
        usuario_data = {
            "nickname": nickname,
            "ranking": "Iniciante",
            "qtdcartas": 0,
            "xp": 0,
            "nivel": 1
        }
        
        usuario_response = supabase.table("usuario").insert(usuario_data).execute()
        
        print("→ Resultado usuario_response:", usuario_response)
        
        if hasattr(usuario_response, "error") and usuario_response.error:
            print("→ Erro ao inserir na tabela Usuario:", usuario_response.error)
            # Se falhar, remover o registro da tabela pessoa para manter consistência
            supabase.table("pessoa").delete().eq("nickname", nickname).execute()
            raise Exception(f"Erro ao inserir na tabela Usuario")

    # Se o tipo for "educador", criar registro na tabela educador
    elif tipo.lower() == "educador":
        print("→ Inserindo na tabela Educador")
        
        educador_data = {
            "nickname": nickname,
            "cargo": "Professor"  # Cargo padrão
        }
        
        educador_response = supabase.table("educador").insert(educador_data).execute()
        
        print("→ Resultado educador_response:", educador_response)
        
        if hasattr(educador_response, "error") and educador_response.error:
            print("→ Erro ao inserir na tabela Educador:", educador_response.error)
            # Se falhar, remover o registro da tabela pessoa para manter consistência
            supabase.table("pessoa").delete().eq("nickname", nickname).execute()
            raise Exception(f"Erro ao inserir na tabela Educador")

    print("→ Criando usuário no Supabase Auth")

    auth_response = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    print("→ Resultado auth_response:", auth_response)

    if not auth_response.user:
        # Se falhar, limpar registros criados
        supabase.table("pessoa").delete().eq("nickname", nickname).execute()
        if tipo.lower() == "usuario":
            supabase.table("usuario").delete().eq("nickname", nickname).execute()
        elif tipo.lower() == "educador":
            supabase.table("educador").delete().eq("nickname", nickname).execute()
        raise Exception("Erro ao criar usuário no Supabase Auth")

    return pessoa_response.data