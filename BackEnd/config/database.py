from auth.supabase_client import supabase

def get_database():
    """
    Retorna a instância do cliente Supabase para operações de banco de dados
    """
    return supabase
