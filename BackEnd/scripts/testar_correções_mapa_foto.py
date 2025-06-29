"""
Script para testar as correções implementadas:
1. Consistência da foto de perfil
2. Exibição de cartas descobertas no mapa
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.carta_model import CartaModel
from models.colecao_model import ColecaoModel
from models.usuario_model import UsuarioModel

def testar_estrutura_cartas():
    """Testar se as cartas têm as informações necessárias para o mapa"""
    print("🗺️  Testando estrutura das cartas para o mapa...")
    
    carta_model = CartaModel()
    result = carta_model.find_all()
    
    if result["success"]:
        cartas = result["data"]
        print(f"Total de cartas encontradas: {len(cartas)}")
        
        # Verificar se as cartas têm localização
        cartas_com_localizacao = [c for c in cartas if c.get("localizacao")]
        print(f"Cartas com localização: {len(cartas_com_localizacao)}")
        
        # Mostrar algumas localizações exemplo
        print("\nLocalizações encontradas:")
        for carta in cartas_com_localizacao[:5]:
            print(f"  - {carta['qrcode']}: {carta['localizacao']}")
        
        return True
    else:
        print(f"❌ Erro ao buscar cartas: {result['error']}")
        return False

def testar_colecao_usuario(nickname="testuser"):
    """Testar se conseguimos buscar a coleção de um usuário"""
    print(f"\n📚 Testando coleção do usuário '{nickname}'...")
    
    colecao_model = ColecaoModel()
    result = colecao_model.get_colecao_usuario(nickname)
    
    if result["success"]:
        colecao = result["data"]
        print(f"Cartas na coleção: {len(colecao)}")
        
        # Mostrar algumas cartas da coleção
        for item in colecao[:3]:
            if isinstance(item, dict) and "carta" in item:
                carta = item["carta"]
                print(f"  - {carta.get('qrcode', 'N/A')}: {carta.get('localizacao', 'Sem localização')}")
            else:
                print(f"  - Item: {item}")
        
        return True
    else:
        print(f"❌ Erro ao buscar coleção: {result['error']}")
        return False

def testar_foto_perfil_usuario(nickname="testuser"):
    """Testar se conseguimos buscar a foto de perfil do usuário"""
    print(f"\n👤 Testando foto de perfil do usuário '{nickname}'...")
    
    usuario_model = UsuarioModel()
    result = usuario_model.find_by_nickname(nickname)
    
    if result["success"]:
        usuario = result["data"]
        if usuario:
            fotoperfil = usuario.get("fotoperfil")
            if fotoperfil:
                print(f"✅ Usuário tem foto de perfil: {fotoperfil[:50]}...")
            else:
                print("⚠️  Usuário não tem foto de perfil configurada")
            return True
        else:
            print(f"❌ Usuário '{nickname}' não encontrado")
            return False
    else:
        print(f"❌ Erro ao buscar usuário: {result['error']}")
        return False

def testar_mapeamento_localizacoes():
    """Testar o mapeamento de localizações conhecidas"""
    print("\n🗺️  Testando mapeamento de localizações...")
    
    # Localizações conhecidas que devem ter coordenadas
    localizacoes_esperadas = [
        "Prédio Principal - ESALQ",
        "Biblioteca Central",
        "Departamento de Ciências Exatas",
        "Jardim Botânico",
        "Museu de Mineralogia"
    ]
    
    carta_model = CartaModel()
    
    for localizacao in localizacoes_esperadas:
        result = carta_model.find_by_localizacao(localizacao)
        if result["success"] and result["data"]:
            print(f"✅ Localização '{localizacao}': {len(result['data'])} carta(s)")
        else:
            print(f"⚠️  Localização '{localizacao}': nenhuma carta encontrada")

def main():
    print("🧪 Testando correções implementadas...\n")
    
    # Teste 1: Estrutura das cartas
    teste1 = testar_estrutura_cartas()
    
    # Teste 2: Coleção do usuário
    teste2 = testar_colecao_usuario()
    
    # Teste 3: Foto de perfil
    teste3 = testar_foto_perfil_usuario()
    
    # Teste 4: Mapeamento de localizações
    testar_mapeamento_localizacoes()
    
    print("\n📊 Resumo dos testes:")
    print(f"Estrutura das cartas: {'✅' if teste1 else '❌'}")
    print(f"Coleção do usuário: {'✅' if teste2 else '❌'}")
    print(f"Foto de perfil: {'✅' if teste3 else '❌'}")
    
    if teste1 and teste2:
        print("\n🎉 Sistema está pronto para mostrar cartas descobertas no mapa!")
    else:
        print("\n⚠️  Alguns problemas encontrados. Verifique os logs acima.")

if __name__ == "__main__":
    main()
