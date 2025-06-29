#!/usr/bin/env python3
"""
Script para testar o sistema de registro completo
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.register_user import register_user
from config.database import get_database

def testar_registro():
    # Dados de teste
    test_nickname = "teste_usuario_123"
    test_email = "teste123@example.com"
    test_password = "senha123"
    
    try:
        print("🧪 Testando registro de usuário...")
        
        # Limpar dados de teste anteriores (caso existam)
        db = get_database()
        db.table("usuario").delete().eq("nickname", test_nickname).execute()
        db.table("pessoa").delete().eq("nickname", test_nickname).execute()
        
        # Registrar usuário
        result = register_user(test_nickname, test_email, test_password, "usuario")
        
        print(f"✅ Registro criado: {result}")
        
        # Verificar se foi criado nas duas tabelas
        pessoa_result = db.table("pessoa").select("*").eq("nickname", test_nickname).execute()
        usuario_result = db.table("usuario").select("*").eq("nickname", test_nickname).execute()
        
        print(f"📋 Pessoa: {pessoa_result.data}")
        print(f"👤 Usuario: {usuario_result.data}")
        
        if pessoa_result.data and usuario_result.data:
            print("✅ Teste PASSOU - Usuário criado em ambas as tabelas!")
        else:
            print("❌ Teste FALHOU - Usuário não foi criado corretamente")
            
        # Limpar dados de teste
        db.table("usuario").delete().eq("nickname", test_nickname).execute()
        db.table("pessoa").delete().eq("nickname", test_nickname).execute()
        print("🧹 Dados de teste limpos")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    testar_registro()
