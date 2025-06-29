#!/usr/bin/env python3
"""
Script para verificar a estrutura da tabela usuario e sincronizar
usuários da tabela pessoa que não existem na tabela usuario
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.database import get_database

def verificar_estrutura_usuario():
    """Verificar a estrutura da tabela usuario"""
    db = get_database()
    
    print("Estrutura da tabela 'usuario':")
    print("-" * 40)
    try:
        # Tentar buscar um registro para ver os campos disponíveis
        result = db.table("usuario").select("*").limit(1).execute()
        if result.data:
            print("Campos disponíveis:")
            for key in result.data[0].keys():
                print(f"  - {key}")
        else:
            print("Tabela vazia, não é possível determinar a estrutura")
    except Exception as e:
        print(f"Erro: {e}")

def sincronizar_usuarios():
    """Sincronizar usuários da tabela pessoa para a tabela usuario"""
    db = get_database()
    
    print("\nSincronizando usuários...")
    print("-" * 40)
    
    try:
        # Buscar todos os usuários da tabela pessoa
        pessoas = db.table("pessoa").select("*").execute()
        
        if not pessoas.data:
            print("Nenhum usuário encontrado na tabela pessoa")
            return
        
        for pessoa in pessoas.data:
            nickname = pessoa['nickname']
            
            # Verificar se já existe na tabela usuario
            usuario_existente = db.table("usuario").select("nickname").eq("nickname", nickname).execute()
            
            if not usuario_existente.data:
                print(f"Criando usuário '{nickname}' na tabela usuario...")
                
                # Criar usuário na tabela usuario baseado na pessoa
                novo_usuario = {
                    "nickname": pessoa['nickname'],
                    "ranking": "Explorador Iniciante",  # ranking padrão
                    "xp": 0,  # XP inicial
                    "nivel": 1,  # nível inicial
                    "fotoperfil": None  # sem foto inicial
                }
                
                result = db.table("usuario").insert(novo_usuario).execute()
                
                if hasattr(result, 'error') and result.error:
                    print(f"  ✗ Erro ao criar usuário '{nickname}': {result.error}")
                else:
                    print(f"  ✓ Usuário '{nickname}' criado com sucesso")
            else:
                print(f"Usuário '{nickname}' já existe na tabela usuario")
                
    except Exception as e:
        print(f"Erro durante sincronização: {e}")

def listar_usuarios_ambas_tabelas():
    """Listar usuários de ambas as tabelas para comparação"""
    db = get_database()
    
    print("\nComparação de usuários:")
    print("-" * 40)
    
    try:
        # Buscar pessoas
        pessoas = db.table("pessoa").select("nickname").execute()
        nicknames_pessoa = {p['nickname'] for p in pessoas.data} if pessoas.data else set()
        
        # Buscar usuários  
        usuarios = db.table("usuario").select("nickname").execute()
        nicknames_usuario = {u['nickname'] for u in usuarios.data} if usuarios.data else set()
        
        print(f"Total na tabela pessoa: {len(nicknames_pessoa)}")
        print(f"Total na tabela usuario: {len(nicknames_usuario)}")
        
        # Usuários que existem apenas na pessoa
        apenas_pessoa = nicknames_pessoa - nicknames_usuario
        if apenas_pessoa:
            print(f"\nApenas na tabela pessoa ({len(apenas_pessoa)}):")
            for nick in sorted(apenas_pessoa):
                print(f"  - {nick}")
        
        # Usuários que existem apenas na usuario
        apenas_usuario = nicknames_usuario - nicknames_pessoa
        if apenas_usuario:
            print(f"\nApenas na tabela usuario ({len(apenas_usuario)}):")
            for nick in sorted(apenas_usuario):
                print(f"  - {nick}")
        
        # Usuários que existem em ambas
        em_ambas = nicknames_pessoa & nicknames_usuario
        print(f"\nEm ambas as tabelas ({len(em_ambas)}):")
        for nick in sorted(em_ambas):
            print(f"  - {nick}")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    print("=== SINCRONIZAÇÃO DE USUÁRIOS ===")
    
    verificar_estrutura_usuario()
    listar_usuarios_ambas_tabelas()
    
    print("\n" + "="*50)
    resposta = input("Deseja sincronizar os usuários? (s/n): ").lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        sincronizar_usuarios()
        print("\nVerificação após sincronização:")
        listar_usuarios_ambas_tabelas()
    else:
        print("Sincronização cancelada.")
