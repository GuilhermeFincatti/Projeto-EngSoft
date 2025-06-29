#!/usr/bin/env python3
"""
Script para criar missões de exemplo no sistema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_database
from datetime import datetime, timedelta

def criar_missoes_exemplo():
    try:
        db = get_database()
        
        print("🚀 Criando missões de exemplo...")
        
        # Definir missões de exemplo
        missoes_exemplo = [
            {
                "tipo": "Coletor Iniciante",
                "educador": "Golias",
                "datafim": None
            },
            {
                "tipo": "Caçador de Raras", 
                "educador": "Golias",
                "datafim": None
            },
            {
                "tipo": "Explorador",
                "educador": "Golias", 
                "datafim": None
            },
            {
                "tipo": "Lenda Viva",
                "educador": "Golias",
                "datafim": None
            },
            {
                "tipo": "Veterano",
                "educador": "Golias",
                "datafim": None
            },
            {
                "tipo": "Evento Especial",
                "educador": "Golias",
                "datafim": (datetime.now() + timedelta(days=30)).isoformat()
            }
        ]
        
        # Limpar missões existentes (opcional)
        print("🧹 Limpando missões existentes...")
        db.table("Missao").delete().neq("Codigo", 0).execute()
        db.table("MissaoQtd").delete().neq("Codigo", 0).execute()
        db.table("MissaoRaridade").delete().neq("Codigo", 0).execute()
        
        # Criar missões
        missoes_criadas = []
        for i, missao_data in enumerate(missoes_exemplo, 1):
            try:
                print(f"📝 Criando missão: {missao_data['tipo']}")
                
                # Inserir missão principal
                result = db.table("Missao").insert({
                    "Codigo": i,
                    "DataInicio": datetime.now().isoformat(),
                    "DataFim": missao_data.get("datafim"),
                    "Tipo": missao_data["tipo"],
                    "Educador": missao_data["educador"]
                }).execute()
                
                if result.data:
                    missoes_criadas.append(result.data[0])
                    print(f"✅ Missão {i} criada: {missao_data['tipo']}")
                    
                    # Adicionar requisitos específicos
                    if i == 1:  # Coletor Iniciante
                        db.table("missaoqtd").insert({
                            "codigo": i,
                            "quantidadetotal": 5
                        }).execute()
                        print(f"  ➡️ Requisito: Coletar 5 cartas")
                        
                    elif i == 2:  # Caçador de Raras
                        # Para MissaoRaridade, precisa ser relacionado com CartaRara específica
                        # Vou criar apenas a missão principal por enquanto
                        print(f"  ➡️ Requisito: Encontrar cartas raras (específico)")
                        
                    elif i == 3:  # Explorador
                        db.table("missaoqtd").insert({
                            "codigo": i,
                            "quantidadetotal": 10
                        }).execute()
                        print(f"  ➡️ Requisito: Coletar 10 cartas")
                        
                    elif i == 4:  # Lenda Viva
                        # Para missões de raridade específica, seria melhor criar uma lógica personalizada
                        print(f"  ➡️ Requisito: Encontrar carta lendária (específico)")
                        
                    elif i == 5:  # Veterano
                        db.table("missaoqtd").insert({
                            "codigo": i,
                            "quantidadetotal": 20
                        }).execute()
                        print(f"  ➡️ Requisito: Coletar 20 cartas")
                        
                    elif i == 6:  # Evento Especial
                        print(f"  ➡️ Requisito: Evento especial (específico)")
                        
                else:
                    print(f"❌ Erro ao criar missão {i}")
                    
            except Exception as e:
                print(f"❌ Erro ao criar missão {i}: {e}")
        
        print(f"\n✨ Criadas {len(missoes_criadas)} missões!")
        
        # Verificar missões criadas
        print("\n📋 Verificando missões criadas:")
        missoes_result = db.table("missao").select("*").execute()
        for missao in missoes_result.data:
            print(f"  - {missao['codigo']}: {missao['tipo']} ({missao['educador']})")
        
        print("\n🎯 Sistema de missões configurado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    criar_missoes_exemplo()
