from config.database import get_database

# Teste direto da conexão
db = get_database()

print("Testando conexão com banco...")

# Verificar se a tabela usuario existe e tem dados
try:
    result = db.table("usuario").select("count").execute()
    print(f"Tabela usuario existe: {result}")
except Exception as e:
    print(f"Erro ao acessar tabela usuario: {e}")

# Verificar se existem usuários
try:
    result = db.table("usuario").select("*").limit(5).execute()
    print(f"Usuários encontrados: {len(result.data) if result.data else 0}")
    print(f"Primeiros usuários: {result.data[:3] if result.data else 'Nenhum'}")
except Exception as e:
    print(f"Erro ao buscar usuários: {e}")

# Testar a query específica do leaderboard
try:
    result = db.table("usuario").select("nickname, ranking, xp, nivel, qtdcartas").order("xp", desc=True).limit(10).execute()
    print(f"Leaderboard query resultado: {result}")
    print(f"Dados: {result.data}")
except Exception as e:
    print(f"Erro na query do leaderboard: {e}")

# Verificar se a tabela amizade existe
try:
    result = db.table("amizade").select("count").execute()
    print(f"Tabela amizade existe: {result}")
except Exception as e:
    print(f"Erro ao acessar tabela amizade: {e}")
