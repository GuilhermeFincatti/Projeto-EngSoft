#!/usr/bin/env python3
"""
Script para corrigir usuários existentes que não têm registro na tabela usuario
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_database

def corrigir_usuarios_existentes():
    db = get_database()
    
    try:
        # Buscar todas as pessoas do tipo "usuario"
        pessoas_result = db.table("pessoa").select("*").eq("tipo", "usuario").execute()
        
        print(f"Encontradas {len(pessoas_result.data)} pessoas do tipo 'usuario'")
        
        for pessoa in pessoas_result.data:
            nickname = pessoa["nickname"]
            
            # Verificar se já existe na tabela usuario
            usuario_result = db.table("usuario").select("*").eq("nickname", nickname).execute()
            
            if not usuario_result.data:
                # Criar registro na tabela usuario
                usuario_data = {
                    "nickname": nickname,
                    "ranking": "Iniciante",
                    "qtdcartas": 0
                }
                
                insert_result = db.table("usuario").insert(usuario_data).execute()
                
                if hasattr(insert_result, 'error') and insert_result.error:
                    print(f"❌ Erro ao criar usuário {nickname}: {insert_result.error}")
                else:
                    print(f"✅ Usuário {nickname} criado na tabela usuario")
            else:
                print(f"ℹ️  Usuário {nickname} já existe na tabela usuario")
                
        # Buscar todas as pessoas do tipo "educador"
        educadores_result = db.table("pessoa").select("*").eq("tipo", "educador").execute()
        
        print(f"Encontradas {len(educadores_result.data)} pessoas do tipo 'educador'")
        
        for pessoa in educadores_result.data:
            nickname = pessoa["nickname"]
            
            # Verificar se já existe na tabela educador
            educador_result = db.table("educador").select("*").eq("nickname", nickname).execute()
            
            if not educador_result.data:
                # Criar registro na tabela educador
                educador_data = {
                    "nickname": nickname,
                    "cargo": "Professor"  # Cargo padrão
                }
                
                insert_result = db.table("educador").insert(educador_data).execute()
                
                if hasattr(insert_result, 'error') and insert_result.error:
                    print(f"❌ Erro ao criar educador {nickname}: {insert_result.error}")
                else:
                    print(f"✅ Educador {nickname} criado na tabela educador")
            else:
                print(f"ℹ️  Educador {nickname} já existe na tabela educador")
                
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🔧 Corrigindo usuários existentes...")
    corrigir_usuarios_existentes()
    print("✨ Processo concluído!")
