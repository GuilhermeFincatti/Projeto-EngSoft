"""
Script para popular o banco de dados com cartas de exemplo
Execute este script após configurar o banco de dados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.carta_model import CartaModel

def criar_cartas_exemplo():
    """Criar cartas de exemplo no banco de dados"""
    carta_model = CartaModel()
    
    cartas_exemplo = [
        {
            "qrcode": "QR001",
            "raridade": "comum",
            "imagem": "https://example.com/sol.png",
            "localizacao": "Prédio Principal - ESALQ"
        },
        {
            "qrcode": "QR002", 
            "raridade": "rara",
            "imagem": "https://example.com/lua.png",
            "localizacao": "Biblioteca Central"
        },
        {
            "qrcode": "QR003",
            "raridade": "comum", 
            "imagem": "https://example.com/mercurio.png",
            "localizacao": "Departamento de Ciências Exatas"
        },
        {
            "qrcode": "QR004",
            "raridade": "incomum",
            "imagem": "https://example.com/venus.png", 
            "localizacao": "Jardim Botânico"
        },
        {
            "qrcode": "QR005",
            "raridade": "rara",
            "imagem": "https://example.com/terra.png",
            "localizacao": "Museu de Mineralogia"
        },
        {
            "qrcode": "QR006",
            "raridade": "incomum",
            "imagem": "https://example.com/marte.png",
            "localizacao": "Departamento de Solos"
        },
        {
            "qrcode": "QR007",
            "raridade": "lendária",
            "imagem": "https://example.com/jupiter.png",
            "localizacao": "Observatório Astronômico"
        },
        {
            "qrcode": "QR008",
            "raridade": "lendária", 
            "imagem": "https://example.com/saturno.png",
            "localizacao": "Planetário ESALQ"
        },
        {
            "qrcode": "QR009",
            "raridade": "épica",
            "imagem": "https://example.com/urano.png",
            "localizacao": "Laboratório de Física"
        },
        {
            "qrcode": "QR010",
            "raridade": "épica",
            "imagem": "https://example.com/netuno.png", 
            "localizacao": "Centro de Pesquisas"
        },
        {
            "qrcode": "QR011",
            "raridade": "rara",
            "imagem": "https://example.com/plutao.png",
            "localizacao": "Museu de História Natural"
        }
    ]
    
    print("Criando cartas de exemplo...")
    
    for carta_data in cartas_exemplo:
        result = carta_model.create(carta_data)
        if result["success"]:
            print(f"✅ Carta {carta_data['qrcode']} criada com sucesso")
        else:
            if "já existe" in result["error"]:
                print(f"⚠️ Carta {carta_data['qrcode']} já existe")
            else:
                print(f"❌ Erro ao criar carta {carta_data['qrcode']}: {result['error']}")
    
    print("\n✨ Processo de criação de cartas concluído!")

if __name__ == "__main__":
    criar_cartas_exemplo()
