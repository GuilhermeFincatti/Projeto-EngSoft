"""
Script para corrigir cartas que têm coordenadas no campo localização
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_database

def corrigir_cartas_com_coordenadas_na_localizacao():
    """Corrigir cartas que têm coordenadas no campo localização"""
    print("🔧 Corrigindo cartas com coordenadas na localização...")
    
    db = get_database()
    
    try:
        # Buscar cartas que têm coordenadas na localização (formato "-22,xxx,-47,xxx")
        cartas_result = db.table("carta").select("qrcode, localizacao, latitude, longitude").execute()
        
        if not cartas_result.data:
            print("❌ Nenhuma carta encontrada")
            return False
        
        cartas_corrigidas = 0
        
        for carta in cartas_result.data:
            qrcode = carta['qrcode']
            localizacao = carta['localizacao']
            latitude_atual = carta.get('latitude')
            longitude_atual = carta.get('longitude')
            
            # Verificar se a localização tem formato de coordenadas
            if isinstance(localizacao, str) and localizacao.startswith('-22,') and ',-47,' in localizacao:
                try:
                    # Extrair coordenadas da string da localização
                    partes = localizacao.split(',')
                    if len(partes) >= 4:
                        lat_str = f"{partes[0]}.{partes[1]}"
                        lng_str = f"{partes[2]}.{partes[3]}"
                        
                        latitude = float(lat_str)
                        longitude = float(lng_str)
                        
                        # Definir localização baseada nas coordenadas aproximadas
                        if abs(latitude + 22.7093) < 0.001 and abs(longitude + 47.6322) < 0.001:
                            nova_localizacao = "Prédio Principal - ESALQ"
                        elif abs(latitude + 22.7107) < 0.001:
                            nova_localizacao = "Departamento de Solos"
                        elif abs(latitude + 22.7087) < 0.001:
                            nova_localizacao = "Biblioteca Central"
                        elif abs(latitude + 22.7085) < 0.001:
                            nova_localizacao = "Jardim Botânico"
                        elif abs(latitude + 22.7089) < 0.001:
                            nova_localizacao = "Centro de Pesquisas"
                        elif abs(latitude + 22.7104) < 0.001:
                            nova_localizacao = "Laboratório de Física"
                        else:
                            nova_localizacao = f"Localização {qrcode}"
                        
                        # Atualizar carta
                        update_result = db.table("carta").update({
                            'latitude': latitude,
                            'longitude': longitude,
                            'localizacao': nova_localizacao
                        }).eq('qrcode', qrcode).execute()
                        
                        if hasattr(update_result, 'error') and update_result.error:
                            print(f"❌ Erro ao atualizar carta {qrcode}: {update_result.error}")
                        else:
                            print(f"✅ Carta {qrcode} corrigida: {nova_localizacao} ({latitude}, {longitude})")
                            cartas_corrigidas += 1
                        
                except ValueError as ve:
                    print(f"⚠️  Erro ao processar coordenadas da carta {qrcode}: {ve}")
                except Exception as e:
                    print(f"❌ Erro inesperado com carta {qrcode}: {e}")
        
        print(f"\n🎉 Processo concluído! {cartas_corrigidas} cartas corrigidas")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o processo: {str(e)}")
        return False

def main():
    print("🚀 Iniciando correção de cartas com coordenadas na localização...\n")
    
    sucesso = corrigir_cartas_com_coordenadas_na_localizacao()
    
    if sucesso:
        print("\n📊 Verificação final...")
        # Verificar estado final
        db = get_database()
        cartas_result = db.table("carta").select("qrcode, localizacao, latitude, longitude").execute()
        
        com_coordenadas = 0
        sem_coordenadas = 0
        
        for carta in cartas_result.data:
            latitude = carta.get('latitude')
            longitude = carta.get('longitude')
            
            if latitude is not None and longitude is not None:
                com_coordenadas += 1
            else:
                sem_coordenadas += 1
        
        print(f"Cartas com coordenadas: {com_coordenadas}")
        print(f"Cartas sem coordenadas: {sem_coordenadas}")

if __name__ == "__main__":
    main()
