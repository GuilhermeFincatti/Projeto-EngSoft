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
