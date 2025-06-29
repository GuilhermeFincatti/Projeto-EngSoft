#!/usr/bin/env python3
"""
Script para verificar e criar a tabela coleta no Supabase
"""
from config.database import get_database

def verificar_e_criar_tabela():
    db = get_database()
    
    try:
        # Tentar fazer uma query simples na tabela coleta
        result = db.table("coleta").select("*").limit(1).execute()
        print("✅ Tabela 'coleta' existe e está acessível")
        print(f"Dados atuais: {result.data}")
        
    except Exception as e:
        print(f"❌ Erro ao acessar tabela 'coleta': {e}")
        print("Tentando criar a tabela...")
        
        try:
            # Criar a tabela via RPC se possível
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS coleta (
                usuario VARCHAR REFERENCES pessoa(nickname) ON DELETE CASCADE,
                qrcode VARCHAR REFERENCES carta(qrcode) ON DELETE CASCADE,
                quantidade INT DEFAULT 1,
                PRIMARY KEY (usuario, qrcode)
            );
            """
            
            # Como o Supabase Python não suporta SQL direto, vamos apenas reportar
            print("❌ Não é possível criar tabela via Python client")
            print("Execute este SQL no Dashboard do Supabase:")
            print(create_table_sql)
            
        except Exception as create_error:
            print(f"❌ Erro ao criar tabela: {create_error}")

if __name__ == "__main__":
    verificar_e_criar_tabela()
