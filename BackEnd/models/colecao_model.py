from typing import Optional, Dict, Any, List
from config.database import get_database

class ColecaoModel:
    def __init__(self):
        self.db = get_database()
    
    def adicionar_carta(self, usuario: str, qrcode: str, quantidade: int = 1) -> Dict[str, Any]:
        """Adicionar carta à coleção do usuário"""
        try:
            # Verificar se a carta já existe na coleção
            existing = self.get_carta_usuario(usuario, qrcode)
            
            if existing["success"]:
                # Se já existe, atualizar quantidade
                nova_quantidade = existing["data"]["quantidade"] + quantidade
                print(f"DEBUG ColecaoModel: Atualizando quantidade para {nova_quantidade}")
                result = (self.db.table("coleta")
                         .update({"quantidade": nova_quantidade})
                         .eq("usuario", usuario)
                         .eq("qrcode", qrcode)
                         .execute())
            else:
                # Se não existe, inserir nova entrada
                coleta_data = {
                    "usuario": usuario,
                    "qrcode": qrcode,
                    "quantidade": quantidade
                }
                print(f"DEBUG ColecaoModel: Inserindo nova entrada: {coleta_data}")
                result = self.db.table("coleta").insert(coleta_data).execute()
            
            print(f"DEBUG ColecaoModel: Resultado da operação: {result}")
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao adicionar carta: {result.error}")
            
            # Atualizar contador de cartas do usuário
            self._atualizar_contador_cartas(usuario)
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            print(f"ERROR ColecaoModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    def get_colecao_usuario(self, usuario: str) -> Dict[str, Any]:
        """Buscar todas as cartas coletadas por um usuário"""
        try:
            result = (self.db.table("coleta")
                     .select("""
                         qrcode,
                         quantidade,
                         carta:qrcode (
                             qrcode,
                             raridade,
                             imagem,
                             audio,
                             localizacao,
                             descricao,
                             latitude,
                             longitude
                         )
                     """)
                     .eq("usuario", usuario)
                     .execute())
            
            # Adicionar nomes dinâmicos às cartas
            if result.data:
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
                
                for item in result.data:
                    if item.get("carta"):
                        qrcode = item["carta"]["qrcode"]
                        item["carta"]["nome"] = cartas_nomes.get(qrcode, f"Carta {qrcode}")
                        
                        # Adicionar coordenadas se disponíveis
                        carta = item["carta"]
                        if carta.get("latitude") is not None and carta.get("longitude") is not None:
                            carta["coordinates"] = {
                                "latitude": float(carta["latitude"]),
                                "longitude": float(carta["longitude"])
                            }
            
            return {"success": True, "data": result.data}
        except Exception as e:
            print(f"ERROR ColecaoModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    def get_carta_usuario(self, usuario: str, qrcode: str) -> Dict[str, Any]:
        """Verificar se usuário possui uma carta específica"""
        try:
            print(f"DEBUG get_carta_usuario: Buscando carta {qrcode} para usuario {usuario}")
            result = (self.db.table("coleta")
                     .select("*")
                     .eq("usuario", usuario)
                     .eq("qrcode", qrcode)
                     .single()
                     .execute())
            
            print(f"DEBUG get_carta_usuario: Resultado: {result}")
            
            if not result.data:
                return {"success": False, "error": "Carta não encontrada na coleção"}
            
            return {"success": True, "data": result.data}
        except Exception as e:
            print(f"ERROR ColecaoModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    def remover_carta(self, usuario: str, qrcode: str, quantidade: int = 1) -> Dict[str, Any]:
        """Remover carta da coleção do usuário"""
        try:
            existing = self.get_carta_usuario(usuario, qrcode)
            
            if not existing["success"]:
                return {"success": False, "error": "Carta não encontrada na coleção"}
            
            quantidade_atual = existing["data"]["quantidade"]
            
            if quantidade_atual <= quantidade:
                # Remover completamente
                result = (self.db.table("coleta")
                         .delete()
                         .eq("usuario", usuario)
                         .eq("qrcode", qrcode)
                         .execute())
            else:
                # Diminuir quantidade
                nova_quantidade = quantidade_atual - quantidade
                result = (self.db.table("coleta")
                         .update({"quantidade": nova_quantidade})
                         .eq("usuario", usuario)
                         .eq("qrcode", qrcode)
                         .execute())
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao remover carta: {result.error}")
            
            # Atualizar contador de cartas do usuário
            self._atualizar_contador_cartas(usuario)
            
            return {"success": True, "data": result.data}
        except Exception as e:
            print(f"ERROR ColecaoModel: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    def get_estatisticas_colecao(self, usuario: str) -> Dict[str, Any]:
        """Buscar estatísticas da coleção do usuário"""
        try:
            # Total de cartas coletadas
            total_result = (self.db.table("coleta")
                           .select("quantidade")
                           .eq("usuario", usuario)
                           .execute())
            
            total_cartas = sum(item["quantidade"] for item in total_result.data)
            
            # Cartas únicas
            cartas_unicas = len(total_result.data)
            
            # Cartas por raridade
            raridade_result = (self.db.table("coleta")
                              .select("""
                                  quantidade,
                                  carta:qrcode (raridade)
                              """)
                              .eq("usuario", usuario)
                              .execute())
            
            raridades = {}
            for item in raridade_result.data:
                raridade = item["carta"]["raridade"]
                quantidade = item["quantidade"]
                raridades[raridade] = raridades.get(raridade, 0) + quantidade
            
            return {
                "success": True, 
                "data": {
                    "total_cartas": total_cartas,
                    "cartas_unicas": cartas_unicas,
                    "por_raridade": raridades
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def limpar_colecao(self, usuario: str) -> Dict[str, Any]:
        """Limpar toda a coleção do usuário"""
        try:
            result = (self.db.table("coleta")
                     .delete()
                     .eq("usuario", usuario)
                     .execute())
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao limpar coleção: {result.error}")
            
            # Atualizar contador de cartas do usuário
            self._atualizar_contador_cartas(usuario)
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _atualizar_contador_cartas(self, usuario: str) -> None:
        """Atualizar o contador QtdCartas na tabela Usuario"""
        try:
            # Calcular total de cartas
            total_result = (self.db.table("coleta")
                           .select("quantidade")
                           .eq("usuario", usuario)
                           .execute())
            
            total_cartas = sum(item["quantidade"] for item in total_result.data)
            
            # Atualizar na tabela usuario
            self.db.table("usuario").update({"qtdcartas": total_cartas}).eq("nickname", usuario).execute()
        except Exception as e:
            print(f"Erro ao atualizar contador de cartas: {e}")
