#!/usr/bin/env python3
"""
Script para verificar se um usuário existe nas tabelas pessoa e usuario
para debug do sistema de amizade
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.database import get_database

def verificar_usuario(nickname):
    """Verificar se um usuário existe nas tabelas pessoa e usuario"""
    db = get_database()
    
    print(f"Verificando usuário: {nickname}")
    print("-" * 50)
    
    # Verificar na tabela pessoa
    print("1. Verificando na tabela 'pessoa':")
    try:
        pessoa_result = db.table("pessoa").select("*").eq("nickname", nickname).execute()
        if pessoa_result.data:
            print(f"   ✓ Encontrado na tabela pessoa:")
            for key, value in pessoa_result.data[0].items():
                print(f"     {key}: {value}")
        else:
            print(f"   ✗ NÃO encontrado na tabela pessoa")
    except Exception as e:
        print(f"   ✗ Erro ao consultar tabela pessoa: {e}")
    
    print()
    
    # Verificar na tabela usuario
    print("2. Verificando na tabela 'usuario':")
    try:
        usuario_result = db.table("usuario").select("*").eq("nickname", nickname).execute()
        if usuario_result.data:
            print(f"   ✓ Encontrado na tabela usuario:")
            for key, value in usuario_result.data[0].items():
                print(f"     {key}: {value}")
        else:
            print(f"   ✗ NÃO encontrado na tabela usuario")
    except Exception as e:
        print(f"   ✗ Erro ao consultar tabela usuario: {e}")
    
    print()
    
    # Verificar se há discrepâncias
    pessoa_exists = pessoa_result.data if 'pessoa_result' in locals() else False
    usuario_exists = usuario_result.data if 'usuario_result' in locals() else False
    
    if pessoa_exists and not usuario_exists:
        print("⚠️  PROBLEMA: Usuário existe na tabela 'pessoa' mas NÃO na tabela 'usuario'")
        print("   Isso pode causar erros de chave estrangeira no sistema de amizade.")
        return False
    elif not pessoa_exists and usuario_exists:
        print("⚠️  PROBLEMA: Usuário existe na tabela 'usuario' mas NÃO na tabela 'pessoa'")
        print("   Isso pode causar problemas de autenticação.")
        return False
    elif pessoa_exists and usuario_exists:
        print("✓ OK: Usuário existe em ambas as tabelas")
        return True
    else:
        print("✗ PROBLEMA: Usuário NÃO existe em nenhuma das tabelas")
        return False

def listar_usuarios_pessoa():
    """Listar todos os usuários da tabela pessoa"""
    db = get_database()
    
    print("Usuários na tabela 'pessoa':")
    print("-" * 30)
    try:
        pessoas = db.table("pessoa").select("nickname, email").execute()
        if pessoas.data:
            for pessoa in pessoas.data:
                print(f"  - {pessoa['nickname']} ({pessoa['email']})")
        else:
            print("  Nenhum usuário encontrado")
    except Exception as e:
        print(f"  Erro: {e}")

def listar_usuarios_usuario():
    """Listar todos os usuários da tabela usuario"""
    db = get_database()
    
    print("Usuários na tabela 'usuario':")
    print("-" * 30)
    try:
        usuarios = db.table("usuario").select("nickname, email").execute()
        if usuarios.data:
            for usuario in usuarios.data:
                print(f"  - {usuario['nickname']} ({usuario.get('email', 'N/A')})")
        else:
            print("  Nenhum usuário encontrado")
    except Exception as e:
        print(f"  Erro: {e}")

if __name__ == "__main__":
    print("=== VERIFICAÇÃO DE USUÁRIO PARA SISTEMA DE AMIZADE ===")
    print()
    
    # Verificar o usuário específico que está causando problema
    nickname_problema = "johnatas2"
    verificar_usuario(nickname_problema)
    
    print("\n" + "="*60 + "\n")
    
    # Listar todos os usuários para comparação
    listar_usuarios_pessoa()
    print()
    listar_usuarios_usuario()
    
    print("\n" + "="*60)
    print("DICA: Se um usuário existe apenas na tabela 'pessoa',")
    print("      você precisa criar um registro correspondente na tabela 'usuario'")
    print("      para que o sistema de amizade funcione corretamente.")
