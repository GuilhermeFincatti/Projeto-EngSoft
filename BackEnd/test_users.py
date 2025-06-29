from config.database import get_database

# Verificar usuários e pessoas
db = get_database()

try:
    # Buscar pessoas
    pessoas = db.table("pessoa").select("*").execute()
    print("Pessoas:")
    for pessoa in pessoas.data:
        print(f"  - {pessoa}")
    
    # Buscar usuários
    usuarios = db.table("usuario").select("*").execute()
    print("\nUsuários:")
    for usuario in usuarios.data:
        print(f"  - {usuario}")
        
except Exception as e:
    print(f"Erro: {e}")
