"""
Script para testar o endpoint de coleção com as novas coordenadas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.colecao_model import ColecaoModel
import json

def testar_colecao_com_coordenadas(nickname="testuser"):
    """Testar se a coleção retorna cartas com coordenadas"""
    print(f"🧪 Testando coleção com coordenadas para '{nickname}'...")
    
    colecao_model = ColecaoModel()
    result = colecao_model.get_colecao_usuario(nickname)
    
    if result["success"]:
        colecao = result["data"]
        print(f"✅ Coleção encontrada com {len(colecao)} item(s)")
        
        if len(colecao) > 0:
            print("\n📍 Verificando coordenadas nas cartas:")
            for i, item in enumerate(colecao[:3]):  # Mostrar apenas os primeiros 3
                carta = item.get("carta", {})
                if carta:
                    qrcode = carta.get("qrcode", "N/A")
                    nome = carta.get("nome", "Sem nome")
                    localizacao = carta.get("localizacao", "Sem localização")
                    coordinates = carta.get("coordinates", None)
                    
                    print(f"  {i+1}. {qrcode} - {nome}")
                    print(f"     Localização: {localizacao}")
                    
                    if coordinates:
                        lat = coordinates.get("latitude")
                        lng = coordinates.get("longitude")
                        print(f"     ✅ Coordenadas: ({lat}, {lng})")
                    else:
                        print(f"     ❌ Sem coordenadas")
                    print()
            
            # Contar cartas com coordenadas
            cartas_com_coordenadas = sum(1 for item in colecao 
                                       if item.get("carta", {}).get("coordinates"))
            
            print(f"📊 Resumo:")
            print(f"Total de cartas: {len(colecao)}")
            print(f"Cartas com coordenadas: {cartas_com_coordenadas}")
            print(f"Cartas sem coordenadas: {len(colecao) - cartas_com_coordenadas}")
            
            if cartas_com_coordenadas > 0:
                print(f"🎉 Sistema funcionando! {cartas_com_coordenadas} cartas podem ser exibidas no mapa")
                return True
            else:
                print(f"⚠️  Nenhuma carta tem coordenadas para exibir no mapa")
                return False
        else:
            print("ℹ️  Usuário não tem cartas na coleção (normal para usuário de teste)")
            return True
    else:
        print(f"❌ Erro ao buscar coleção: {result['error']}")
        return False

def criar_usuario_teste_com_cartas():
    """Criar algumas cartas na coleção do usuário de teste para verificar"""
    print("🛠️  Adicionando cartas para teste...")
    
    colecao_model = ColecaoModel()
    
    # Adicionar algumas cartas de teste
    cartas_teste = ["QR001", "QR002", "QR003"]
    
    for qrcode in cartas_teste:
        result = colecao_model.adicionar_carta("testuser", qrcode, 1)
        if result["success"]:
            print(f"✅ Carta {qrcode} adicionada")
        else:
            if "já existe" in str(result.get("error", "")):
                print(f"ℹ️  Carta {qrcode} já existe na coleção")
            else:
                print(f"❌ Erro ao adicionar carta {qrcode}: {result['error']}")

def main():
    print("🚀 Testando endpoint de coleção com coordenadas...\n")
    
    # Primeiro, criar algumas cartas na coleção para teste
    criar_usuario_teste_com_cartas()
    
    print()
    
    # Testar se a coleção retorna coordenadas
    sucesso = testar_colecao_com_coordenadas()
    
    if sucesso:
        print("\n✅ Teste concluído com sucesso!")
        print("🗺️  O home.jsx agora pode usar getMinhaColecao() para exibir cartas no mapa")
    else:
        print("\n❌ Teste falhou. Verifique a implementação.")

if __name__ == "__main__":
    main()
