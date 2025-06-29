#!/usr/bin/env python3
"""
Script para adicionar descrições às cartas existentes
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_database

def atualizar_descricoes_cartas():
    db = get_database()
    
    # Descrições detalhadas para cada carta
    descricoes = {
        "QR001": "O Sol, nossa estrela central, é uma gigantesca esfera de plasma que fornece luz e calor essenciais para a vida na Terra. Com uma temperatura superficial de 5.778K, é classificado como uma estrela anã amarela do tipo G.",
        
        "QR002": "A Lua é o único satélite natural da Terra e o quinto maior satélite do Sistema Solar. Suas fases lunares influenciam as marés oceânicas e têm sido objeto de fascínio humano por milênios.",
        
        "QR003": "Mercúrio é o menor planeta do Sistema Solar e o mais próximo do Sol. Sua superfície apresenta crateras semelhantes às da Lua, com temperaturas extremas que variam de -173°C a 427°C.",
        
        "QR004": "Vênus, conhecido como 'Estrela da Manhã' ou 'Estrela da Tarde', é o planeta mais quente do Sistema Solar devido ao seu efeito estufa extremo. Sua atmosfera densa é composta principalmente de dióxido de carbono.",
        
        "QR005": "A Terra é o terceiro planeta do Sistema Solar e o único conhecido por abrigar vida. Possui 71% de sua superfície coberta por água e uma atmosfera rica em oxigênio e nitrogênio.",
        
        "QR006": "Marte, o 'Planeta Vermelho', possui a maior montanha do Sistema Solar, o Monte Olimpo. Evidências sugerem que já teve água líquida em sua superfície, tornando-o alvo de missões espaciais em busca de vida.",
        
        "QR007": "Júpiter é o maior planeta do Sistema Solar, com uma massa maior que todos os outros planetas combinados. Sua Grande Mancha Vermelha é uma tempestade que perdura há séculos.",
        
        "QR008": "Saturno é famoso por seus espetaculares anéis compostos de gelo e rocha. É o segundo maior planeta do Sistema Solar e possui mais de 80 luas conhecidas, incluindo Titã, que possui uma atmosfera densa.",
        
        "QR009": "Urano é único por sua rotação lateral - seus polos apontam para o Sol durante suas estações. Este gigante gelado possui um sistema de anéis tênues e 27 luas conhecidas.",
        
        "QR010": "Netuno, o planeta mais distante do Sol, possui os ventos mais fortes do Sistema Solar, chegando a 2.100 km/h. Sua cor azul característica é resultado do metano em sua atmosfera.",
        
        "QR011": "Plutão, reclassificado como planeta anão em 2006, possui uma lua chamada Caronte que é quase metade do seu tamanho. Localizado no Cinturão de Kuiper, representa os mistérios das regiões mais distantes do nosso sistema planetário."
    }
    
    try:
        print("🔄 Atualizando descrições das cartas...")
        
        for qrcode, descricao in descricoes.items():
            # Atualizar cada carta
            result = (db.table("carta")
                     .update({"descricao": descricao})
                     .eq("qrcode", qrcode)
                     .execute())
            
            if hasattr(result, 'error') and result.error:
                print(f"❌ Erro ao atualizar carta {qrcode}: {result.error}")
            else:
                print(f"✅ Carta {qrcode} atualizada com descrição")
        
        print("✨ Todas as descrições foram atualizadas!")
        
        # Verificar resultado
        cartas_result = db.table("carta").select("qrcode, descricao").execute()
        print(f"\n📋 Total de cartas com descrição: {len([c for c in cartas_result.data if c.get('descricao')])}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    atualizar_descricoes_cartas()
