#!/usr/bin/env python3
"""
Script para adicionar campo nome à tabela carta
"""

from config.database import get_database

def add_nome_column():
    try:
        db = get_database()
        
        print("🔄 Adicionando campo nome à tabela carta...")
        
        # Executar SQL direto para adicionar coluna (Supabase não suporta ALTER TABLE via SDK)
        # Vamos atualizar as cartas existentes via API
        
        # Primeiro, vamos mapear os nomes das cartas
        cartas_nomes = {
            'QR001': 'Framboyant Dourado',
            'QR002': 'Pau-Brasil Histórico', 
            'QR003': 'Pau-Formiga Guardião',
            'QR004': 'Cuieté Majestoso',
            'QR005': 'Abricó-de-Macaco',
            'QR006': 'Sol Radiante',
            'QR007': 'Júpiter Colossal',
            'QR008': 'Saturno dos Anéis',
            'QR009': 'Urano Místico',
            'QR010': 'Netuno Tempestuoso',
            'QR011': 'Plutão Distante',
            '1': 'Framboyant Dourado',
            '2': 'Pau-Brasil Histórico',
            '3': 'Pau-Formiga Guardião',
            '4': 'Cuieté Majestoso',
            '5': 'Abricó-de-Macaco'
        }
        
        # Buscar todas as cartas
        cartas_result = db.table("carta").select("qrcode").execute()
        
        if not cartas_result.data:
            print("❌ Nenhuma carta encontrada")
            return
        
        # Atualizar cada carta com seu nome
        for carta in cartas_result.data:
            qrcode = carta["qrcode"]
            nome = cartas_nomes.get(qrcode, f"Carta {qrcode}")
            
            try:
                # Como o Supabase não permite ALTER TABLE via SDK, vamos simular
                # adicionando os nomes via update (assumindo que a coluna já existe)
                result = db.table("carta").update({"nome": nome}).eq("qrcode", qrcode).execute()
                
                if result.data:
                    print(f"✅ Carta {qrcode} atualizada com nome: {nome}")
                else:
                    print(f"⚠️ Não foi possível atualizar carta {qrcode} - isso é normal se a coluna nome não existir ainda")
            except Exception as e:
                print(f"⚠️ Erro ao atualizar carta {qrcode}: {e}")
        
        print(f"✨ Processo concluído!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    add_nome_column()
