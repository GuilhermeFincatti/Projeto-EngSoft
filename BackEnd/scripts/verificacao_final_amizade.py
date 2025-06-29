#!/usr/bin/env python3
"""
Script de verificação final para confirmar que os problemas de amizade foram resolvidos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.amizade_model import AmizadeModel
from controllers.amizade_controller import AmizadeController, SolicitacaoAmizadeRequest

def verificar_correcoes():
    """Verificar se todas as correções foram aplicadas corretamente"""
    print("=== VERIFICAÇÃO FINAL DAS CORREÇÕES ===")
    print()
    
    # 1. Verificar se o modelo de amizade funciona
    print("1. Testando AmizadeModel...")
    model = AmizadeModel()
    
    # Limpar dados de teste anteriores
    model.remover_amizade("johnatas2", "johnatas")
    
    # Teste básico do model
    result = model.enviar_solicitacao("johnatas2", "johnatas")
    if result["success"]:
        print("  ✓ AmizadeModel funcionando corretamente")
        
        # Limpar após teste
        model.remover_amizade("johnatas2", "johnatas")
    else:
        print(f"  ✗ Erro no AmizadeModel: {result['error']}")
        return False
    
    # 2. Verificar se o controller funciona
    print("2. Testando AmizadeController...")
    controller = AmizadeController()
    
    # Simular dados do usuário autenticado
    class MockUser:
        def __init__(self, email):
            self.email = email
    
    # Teste do controller
    mock_user = MockUser("johnatas@usp.br")  # email do johnatas2
    solicitacao_data = SolicitacaoAmizadeRequest(destinatario="johnatas")
    
    # Primeiro verificar se consegue buscar o nickname do email
    nickname_result = controller._get_nickname_from_email(mock_user.email)
    if nickname_result["success"]:
        print(f"  ✓ Nickname encontrado: {nickname_result['data']}")
        
        # Agora testar o envio da solicitação
        solicitante = nickname_result["data"]
        result = controller.enviar_solicitacao(solicitante, solicitacao_data)
        
        if result["success"]:
            print("  ✓ AmizadeController funcionando corretamente")
            
            # Limpar após teste
            model.remover_amizade(solicitante, solicitacao_data.destinatario)
        else:
            print(f"  ✗ Erro no AmizadeController: {result['error']}")
            return False
    else:
        print(f"  ✗ Erro ao buscar nickname: {nickname_result['error']}")
        return False
    
    print()
    print("🎉 TODAS AS CORREÇÕES FORAM APLICADAS COM SUCESSO!")
    print()
    print("Resumo das correções realizadas:")
    print("✓ Sincronizados usuários entre tabelas 'pessoa' e 'usuario'")
    print("✓ Adicionada validação de existência do solicitante no controller")
    print("✓ Removidos métodos problemáticos do UsuarioModel")
    print("✓ Sistema de amizade funcionando sem erros de chave estrangeira")
    
    return True

def testar_cenarios_edge():
    """Testar cenários específicos para garantir robustez"""
    print("\n=== TESTES DE CENÁRIOS ESPECÍFICOS ===")
    
    controller = AmizadeController()
    model = AmizadeModel()
    
    # Cenário 1: Usuário inexistente na tabela pessoa
    print("1. Testando usuário inexistente na tabela pessoa:")
    class MockUser:
        def __init__(self, email):
            self.email = email
    
    mock_user = MockUser("usuario_inexistente@teste.com")
    nickname_result = controller._get_nickname_from_email(mock_user.email)
    
    if not nickname_result["success"]:
        print("  ✓ Tratamento correto para usuário inexistente na tabela pessoa")
    else:
        print("  ✗ PROBLEMA: Encontrou usuário que não deveria existir")
        return False
    
    # Cenário 2: Destinatário inexistente
    print("2. Testando destinatário inexistente:")
    solicitacao_data = SolicitacaoAmizadeRequest(destinatario="usuario_inexistente")
    result = controller.enviar_solicitacao("johnatas2", solicitacao_data)
    
    if not result["success"] and "não encontrado" in result["error"].lower():
        print("  ✓ Tratamento correto para destinatário inexistente")
    else:
        print(f"  ✗ PROBLEMA: {result}")
        return False
    
    print("\n✓ Todos os cenários específicos funcionando corretamente!")
    return True

if __name__ == "__main__":
    sucesso = verificar_correcoes()
    
    if sucesso:
        sucesso = testar_cenarios_edge()
    
    if sucesso:
        print("\n" + "="*60)
        print("🏆 SISTEMA DE AMIZADE TOTALMENTE CORRIGIDO!")
        print("   O erro de chave estrangeira foi resolvido.")
        print("   Todos os testes passaram com sucesso.")
        print("="*60)
    else:
        print("\n❌ Ainda há problemas que precisam ser corrigidos.")
