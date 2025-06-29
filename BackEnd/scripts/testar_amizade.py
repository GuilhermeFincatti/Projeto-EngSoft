#!/usr/bin/env python3
"""
Script para testar o sistema de amizade após as correções
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.amizade_model import AmizadeModel

def testar_solicitacao_amizade():
    """Testar envio de solicitação de amizade"""
    model = AmizadeModel()
    
    print("=== TESTE DE SOLICITAÇÃO DE AMIZADE ===")
    print()
    
    # Teste 1: Solicitação válida
    print("1. Testando solicitação válida (johnatas2 -> johnatas):")
    result = model.enviar_solicitacao("johnatas2", "johnatas")
    if result["success"]:
        print("  ✓ Solicitação enviada com sucesso!")
        print(f"  Dados: {result['data']}")
    else:
        print(f"  ✗ Erro: {result['error']}")
    
    print()
    
    # Teste 2: Tentar enviar a mesma solicitação novamente (deve falhar)
    print("2. Testando solicitação duplicada (deve falhar):")
    result2 = model.enviar_solicitacao("johnatas2", "johnatas")
    if result2["success"]:
        print("  ✗ PROBLEMA: Permitiu solicitação duplicada!")
    else:
        print(f"  ✓ Erro esperado: {result2['error']}")
    
    print()
    
    # Teste 3: Solicitação para usuário inexistente
    print("3. Testando solicitação para usuário inexistente:")
    result3 = model.enviar_solicitacao("johnatas2", "usuario_inexistente")
    if result3["success"]:
        print("  ✗ PROBLEMA: Permitiu solicitação para usuário inexistente!")
    else:
        print(f"  ✓ Erro esperado: {result3['error']}")
    
    print()
    
    # Teste 4: Verificar status da amizade
    print("4. Verificando status da amizade:")
    result4 = model.verificar_status_amizade("johnatas2", "johnatas")
    if result4["success"]:
        print(f"  ✓ Status: {result4['data']}")
    else:
        print(f"  ✗ Erro: {result4['error']}")

def limpar_teste():
    """Limpar dados de teste se necessário"""
    model = AmizadeModel()
    
    print("\n=== LIMPEZA DE DADOS DE TESTE ===")
    print("Removendo possíveis solicitações de teste...")
    
    # Tentar remover amizade/solicitação entre johnatas2 e johnatas
    result = model.remover_amizade("johnatas2", "johnatas")
    if result["success"]:
        print("✓ Dados de teste removidos")
    else:
        print(f"ℹ Nenhum dado de teste para remover: {result['error']}")

if __name__ == "__main__":
    # Limpar dados de teste anteriores
    limpar_teste()
    
    # Executar testes
    testar_solicitacao_amizade()
    
    print("\n" + "="*50)
    print("Teste concluído!")
