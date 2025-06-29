#!/usr/bin/env python3
"""
Script para testar as melhorias da API de cartas e coleção
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_cartas():
    """Testar endpoint de cartas"""
    print("🧪 Testando endpoint /api/cartas...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/cartas", timeout=5)
        if response.status_code == 200:
            cartas = response.json()["data"]
            print(f"✅ {len(cartas)} cartas encontradas")
            
            # Mostrar algumas cartas com nomes e descrições
            for carta in cartas[:3]:
                print(f"  - {carta['qrcode']}: {carta.get('nome', 'Sem nome')} ({carta.get('raridade', 'comum')})")
                print(f"    Descrição: {carta.get('descricao', 'Sem descrição')[:50]}...")
                print(f"    Imagem: {carta.get('imagem', 'Sem imagem')[:50]}...")
                print()
        else:
            print(f"❌ Erro ao buscar cartas: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_colecao():
    """Testar endpoint de coleção (com usuário teste)"""
    print("🧪 Testando endpoint /api/minha-colecao...")
    print("(Apenas mostra estrutura esperada, requer autenticação)")
    
    # Não podemos testar diretamente sem token, mas podemos mostrar a estrutura
    print("Estrutura esperada:")
    print("- qrcode: ID da carta")
    print("- quantidade: Quantidade coletada")
    print("- carta: {nome, raridade, descricao, imagem, audio, localizacao}")

def test_backend_direct():
    """Testar backend diretamente"""
    print("🧪 Testando backend diretamente...")
    
    try:
        from models.carta_model import CartaModel
        from models.colecao_model import ColecaoModel
        
        # Testar cartas
        carta_model = CartaModel()
        cartas_result = carta_model.find_all(3)
        
        if cartas_result["success"]:
            print(f"✅ Backend cartas funcionando: {len(cartas_result['data'])} cartas")
            for carta in cartas_result["data"]:
                print(f"  - {carta['qrcode']}: {carta.get('nome', 'Sem nome')}")
        
        # Testar coleção
        colecao_model = ColecaoModel()
        colecao_result = colecao_model.get_colecao_usuario('johnatas1')
        
        if colecao_result["success"]:
            print(f"✅ Backend coleção funcionando: {len(colecao_result['data'])} cartas na coleção")
            for item in colecao_result["data"]:
                carta = item.get("carta", {})
                print(f"  - {item['qrcode']}: {carta.get('nome', 'Sem nome')} (qtd: {item['quantidade']})")
        
    except Exception as e:
        print(f"❌ Erro no teste direto: {e}")

if __name__ == "__main__":
    print("🚀 Testando melhorias do sistema de cartas\n")
    
    test_backend_direct()
    print()
    test_cartas()
    print()
    test_colecao()
    
    print("\n✨ Teste completo!")
    print("\n📱 Para testar o frontend:")
    print("1. Abra o app ESALQ Explorer")
    print("2. Vá para a tela de Coleção")
    print("3. Verifique se as cartas mostram nomes e imagens")
    print("4. Toque em uma carta coletada para ver detalhes")
