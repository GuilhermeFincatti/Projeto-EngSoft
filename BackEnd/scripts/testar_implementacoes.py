#!/usr/bin/env python3
"""
Script para testar as funcionalidades implementadas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def testar_implementacoes():
    print("🚀 Testando implementações do sistema ESALQ Explorer\n")
    
    # 1. Testar cartas com descrições
    print("1️⃣ Testando cartas com descrições e nomes...")
    try:
        from models.carta_model import CartaModel
        carta_model = CartaModel()
        result = carta_model.find_all(3)
        
        if result["success"]:
            print(f"✅ {len(result['data'])} cartas encontradas")
            for carta in result["data"]:
                print(f"   📍 {carta['qrcode']}: {carta.get('nome', 'Sem nome')}")
                print(f"      Raridade: {carta.get('raridade', 'comum')}")
                print(f"      Descrição: {carta.get('descricao', 'Sem descrição')[:50]}...")
                print()
        else:
            print(f"❌ Erro: {result['error']}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 2. Testar coleção com informações melhoradas
    print("2️⃣ Testando coleção do usuário...")
    try:
        from models.colecao_model import ColecaoModel
        colecao_model = ColecaoModel()
        result = colecao_model.get_colecao_usuario('johnatas1')
        
        if result["success"] and result["data"]:
            print(f"✅ {len(result['data'])} cartas na coleção")
            for item in result["data"]:
                carta = item.get("carta", {})
                print(f"   🃏 {item['qrcode']}: {carta.get('nome', 'Sem nome')} (x{item['quantidade']})")
                print(f"      Raridade: {carta.get('raridade', 'comum')}")
                if carta.get('imagem'):
                    print(f"      🖼️  Tem imagem")
        else:
            print("ℹ️ Coleção vazia ou usuário não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 3. Testar missões
    print("3️⃣ Testando sistema de missões...")
    try:
        from models.missao_model import MissaoModel
        from models.missaoqtd_model import MissaoQtdModel
        
        missao_model = MissaoModel()
        missaoqtd_model = MissaoQtdModel()
        
        missoes_result = missao_model.find_all()
        qtd_result = missaoqtd_model.find_all()
        
        if missoes_result["success"]:
            print(f"✅ {len(missoes_result['data'])} missões encontradas")
            for missao in missoes_result["data"][:3]:
                print(f"   🎯 {missao['codigo']}: {missao['tipo']}")
                print(f"      Educador: {missao['educador']}")
                
                # Verificar se tem requisito de quantidade
                qtd_req = next((q for q in qtd_result.get('data', []) if q.get('codigo') == missao['codigo']), None)
                if qtd_req:
                    print(f"      Requisito: {qtd_req.get('quantidadetotal', 'N/A')} cartas")
                print()
        else:
            print(f"❌ Erro: {missoes_result['error']}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("✨ Teste completo!")
    print("\n📱 Para testar no app:")
    print("1. Abra o ESALQ Explorer")
    print("2. Vá para Coleção - deve mostrar cartas com nomes e imagens")
    print("3. Vá para Missões - deve mostrar missões com progresso")
    print("4. Toque em uma carta coletada para ver detalhes com imagem")

if __name__ == "__main__":
    testar_implementacoes()
