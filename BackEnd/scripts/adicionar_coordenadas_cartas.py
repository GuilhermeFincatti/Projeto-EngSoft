"""
Script para adicionar coordenadas às cartas existentes no banco de dados
Este script aplica a migração diretamente no banco via código Python
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_database

def adicionar_coordenadas_cartas():
    """Adicionar colunas de coordenadas e atualizar cartas existentes"""
    print("🗺️  Adicionando coordenadas às cartas...")
    
    db = get_database()
    
    # Mapeamento de localizações para coordenadas
    coordenadas_por_localizacao = {
        'Prédio Principal - ESALQ': {'latitude': -22.7085, 'longitude': -47.6305},
        'Biblioteca Central': {'latitude': -22.7090, 'longitude': -47.6320},
        'Departamento de Ciências Exatas': {'latitude': -22.7080, 'longitude': -47.6290},
        'Jardim Botânico': {'latitude': -22.7095, 'longitude': -47.6310},
        'Museu de Mineralogia': {'latitude': -22.7075, 'longitude': -47.6325},
        'Departamento de Solos': {'latitude': -22.7100, 'longitude': -47.6300},
        'Observatório Astronômico': {'latitude': -22.7070, 'longitude': -47.6315},
        'Planetário ESALQ': {'latitude': -22.7065, 'longitude': -47.6330},
        'Laboratório de Física': {'latitude': -22.7088, 'longitude': -47.6295},
        'Centro de Pesquisas': {'latitude': -22.7092, 'longitude': -47.6285},
        'Museu de História Natural': {'latitude': -22.7078, 'longitude': -47.6340}
    }
    
    try:
        # Buscar todas as cartas
        cartas_result = db.table("carta").select("qrcode, localizacao, latitude, longitude").execute()
        
        if not cartas_result.data:
            print("❌ Nenhuma carta encontrada")
            return False
        
        print(f"📚 Encontradas {len(cartas_result.data)} cartas")
        
        cartas_atualizadas = 0
        
        for carta in cartas_result.data:
            qrcode = carta['qrcode']
            localizacao = carta['localizacao']
            latitude_atual = carta.get('latitude')
            longitude_atual = carta.get('longitude')
            
            # Se já tem coordenadas, pular
            if latitude_atual is not None and longitude_atual is not None:
                print(f"⏭️  Carta {qrcode} já tem coordenadas")
                continue
            
            # Buscar coordenadas para a localização
            coordenadas = coordenadas_por_localizacao.get(localizacao)
            
            if coordenadas:
                # Atualizar carta com coordenadas
                update_result = db.table("carta").update({
                    'latitude': coordenadas['latitude'],
                    'longitude': coordenadas['longitude']
                }).eq('qrcode', qrcode).execute()
                
                if hasattr(update_result, 'error') and update_result.error:
                    print(f"❌ Erro ao atualizar carta {qrcode}: {update_result.error}")
                else:
                    print(f"✅ Carta {qrcode} ({localizacao}) atualizada com coordenadas")
                    cartas_atualizadas += 1
            else:
                print(f"⚠️  Localização '{localizacao}' da carta {qrcode} não tem coordenadas mapeadas")
        
        print(f"\n🎉 Processo concluído! {cartas_atualizadas} cartas atualizadas com coordenadas")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o processo: {str(e)}")
        return False

def verificar_coordenadas():
    """Verificar quais cartas têm coordenadas"""
    print("\n📊 Verificando coordenadas das cartas...")
    
    db = get_database()
    
    try:
        cartas_result = db.table("carta").select("qrcode, localizacao, latitude, longitude").execute()
        
        if not cartas_result.data:
            print("❌ Nenhuma carta encontrada")
            return
        
        com_coordenadas = 0
        sem_coordenadas = 0
        
        print("\nStatus das coordenadas:")
        for carta in cartas_result.data:
            qrcode = carta['qrcode']
            localizacao = carta['localizacao']
            latitude = carta.get('latitude')
            longitude = carta.get('longitude')
            
            if latitude is not None and longitude is not None:
                print(f"✅ {qrcode}: {localizacao} ({latitude}, {longitude})")
                com_coordenadas += 1
            else:
                print(f"❌ {qrcode}: {localizacao} (sem coordenadas)")
                sem_coordenadas += 1
        
        print(f"\n📈 Resumo:")
        print(f"Cartas com coordenadas: {com_coordenadas}")
        print(f"Cartas sem coordenadas: {sem_coordenadas}")
        print(f"Total: {com_coordenadas + sem_coordenadas}")
        
    except Exception as e:
        print(f"❌ Erro ao verificar coordenadas: {str(e)}")

def main():
    print("🚀 Iniciando processo de adição de coordenadas às cartas...\n")
    
    # Verificar estado atual
    verificar_coordenadas()
    
    # Adicionar coordenadas
    sucesso = adicionar_coordenadas_cartas()
    
    # Verificar estado final
    if sucesso:
        verificar_coordenadas()

if __name__ == "__main__":
    main()
