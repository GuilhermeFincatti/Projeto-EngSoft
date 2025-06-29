from typing import List, Optional, Dict, Any
from config.database import get_database
from datetime import datetime

class MensagemModel:
    def __init__(self):
        self.db = get_database()
    
    def create(self, mensagem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar uma nova mensagem"""
        try:
            # Adicionar timestamp atual
            mensagem_data["datahora"] = datetime.now().isoformat()
            
            result = self.db.table("mensagem").insert(mensagem_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar mensagem: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_destinatario(self, destinatario: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar mensagens por destinatário"""
        try:
            query = (self.db.table("mensagem")
                    .select("*")
                    .eq("destinatario", destinatario)
                    .order("datahora", desc=True))
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_remetente(self, remetente: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar mensagens por remetente"""
        try:
            query = (self.db.table("mensagem")
                    .select("*")
                    .eq("remetente", remetente)
                    .order("datahora", desc=True))
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_conversa(self, usuario1: str, usuario2: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar conversa entre dois usuários"""
        try:
            query = (self.db.table("mensagem")
                    .select("*")
                    .or_(f"and(remetente.eq.{usuario1},destinatario.eq.{usuario2}),and(remetente.eq.{usuario2},destinatario.eq.{usuario1})")
                    .order("datahora", desc=True))
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_all(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar todas as mensagens"""
        try:
            query = self.db.table("mensagem").select("*").order("datahora", desc=True)
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete(self, remetente: str, destinatario: str, datahora: str) -> Dict[str, Any]:
        """Deletar mensagem específica"""
        try:
            result = (self.db.table("mensagem")
                     .delete()
                     .eq("remetente", remetente)
                     .eq("destinatario", destinatario)
                     .eq("datahora", datahora)
                     .execute())
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar mensagem: {result.error}")
            
            return {"success": True, "message": "Mensagem deletada com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_chat_messages(self, usuario1: str, usuario2: str, limit: int = 50) -> Dict[str, Any]:
        """Buscar mensagens de um chat entre dois usuários"""
        try:
            result = (self.db.table("mensagem")
                     .select("""
                         *,
                         carta_ref:carta(qrcode, raridade, imagem, localizacao),
                         troca_ref:trocaid(id, status, cartaoferecida, cartasolicitada)
                     """)
                     .or_(f"and(remetente.eq.{usuario1},destinatario.eq.{usuario2}),and(remetente.eq.{usuario2},destinatario.eq.{usuario1})")
                     .order("datahora", desc=False)
                     .limit(limit)
                     .execute())
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao buscar mensagens: {result.error}")
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_message(self, remetente: str, destinatario: str, texto: str, 
                    tipo: str = "texto", carta: str = None, troca_id: int = None) -> Dict[str, Any]:
        """Enviar uma mensagem (texto, carta ou troca)"""
        try:
            mensagem_data = {
                "remetente": remetente,
                "destinatario": destinatario,
                "texto": texto,
                "tipo": tipo,
                "datahora": datetime.now().isoformat()
            }
            
            if carta:
                mensagem_data["carta"] = carta
            
            if troca_id:
                mensagem_data["trocaid"] = troca_id
            
            result = self.db.table("mensagem").insert(mensagem_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao enviar mensagem: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user_chats(self, usuario: str) -> Dict[str, Any]:
        """Buscar lista de chats do usuário com última mensagem"""
        try:
            # Buscar todas as mensagens do usuário
            result = (self.db.table("mensagem")
                     .select("""
                         remetente,
                         destinatario,
                         datahora,
                         texto,
                         tipo
                     """)
                     .or_(f"remetente.eq.{usuario},destinatario.eq.{usuario}")
                     .order("datahora", desc=True)
                     .execute())
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao buscar chats: {result.error}")
            
            # Agrupar por contato
            chats = {}
            for mensagem in result.data:
                if mensagem["remetente"] == usuario:
                    contato = mensagem["destinatario"]
                else:
                    contato = mensagem["remetente"]
                
                if contato not in chats:
                    chats[contato] = {
                        "contato": contato,
                        "ultima_mensagem": mensagem["texto"],
                        "ultima_data": mensagem["datahora"],
                        "tipo": mensagem["tipo"]
                    }
            
            # Buscar informações dos contatos
            chat_list = []
            for chat in chats.values():
                contato_info = (self.db.table("usuario")
                              .select("nickname, fotoperfil, nivel")
                              .eq("nickname", chat["contato"])
                              .single()
                              .execute())
                
                if contato_info.data:
                    chat["contato_info"] = contato_info.data
                    chat_list.append(chat)
            
            # Ordenar por data da última mensagem
            chat_list.sort(key=lambda x: x["ultima_data"], reverse=True)
            
            return {"success": True, "data": chat_list}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def enviar_mensagem_texto(self, remetente: str, destinatario: str, texto: str) -> Dict[str, Any]:
        """Enviar uma mensagem de texto simples"""
        try:
            mensagem_data = {
                "remetente": remetente,
                "destinatario": destinatario,
                "texto": texto,
                "tipo": "texto",
                "datahora": datetime.now().isoformat()
            }
            
            result = self.db.table("mensagem").insert(mensagem_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao enviar mensagem: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def enviar_mensagem_troca(self, remetente: str, destinatario: str, troca_id: int, 
                              carta_oferecida: str, carta_solicitada: str) -> Dict[str, Any]:
        """Enviar uma mensagem com proposta de troca"""
        try:
            # Buscar nomes das cartas
            carta_of_result = self.db.table("carta").select("*").eq("qrcode", carta_oferecida).single().execute()
            carta_sol_result = self.db.table("carta").select("*").eq("qrcode", carta_solicitada).single().execute()
            
            carta_of_nome = f"Carta {carta_oferecida}"
            carta_sol_nome = f"Carta {carta_solicitada}"
            
            if carta_of_result.data:
                carta_of_nome = self._get_nome_carta(carta_oferecida)
            if carta_sol_result.data:
                carta_sol_nome = self._get_nome_carta(carta_solicitada)
            
            texto = f"💱 Proposta de troca: {carta_of_nome} por {carta_sol_nome}"
            
            mensagem_data = {
                "remetente": remetente,
                "destinatario": destinatario,
                "texto": texto,
                "tipo": "troca",
                "trocaid": troca_id,
                "datahora": datetime.now().isoformat()
            }
            
            result = self.db.table("mensagem").insert(mensagem_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao enviar mensagem de troca: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def enviar_mensagem_carta(self, remetente: str, destinatario: str, qrcode: str, 
                              texto: str = "") -> Dict[str, Any]:
        """Enviar uma mensagem compartilhando uma carta"""
        try:
            nome_carta = self._get_nome_carta(qrcode)
            texto_final = f"🃏 {nome_carta}" + (f": {texto}" if texto else "")
            
            mensagem_data = {
                "remetente": remetente,
                "destinatario": destinatario,
                "texto": texto_final,
                "carta": qrcode,
                "tipo": "carta",
                "datahora": datetime.now().isoformat()
            }
            
            result = self.db.table("mensagem").insert(mensagem_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao enviar mensagem com carta: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_nome_carta(self, qrcode: str) -> str:
        """Obter nome da carta"""
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
        return cartas_nomes.get(qrcode, f"Carta {qrcode}")
