from typing import Optional, Dict, Any
from config.database import get_database
from datetime import datetime

class AdicionaModel:
    def __init__(self):
        self.db = get_database()
    
    def create(self, adiciona_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar nova solicitação de amizade"""
        try:
            # Adicionar timestamp atual
            adiciona_data["datahora"] = datetime.now().isoformat()
            
            result = self.db.table("adiciona").insert(adiciona_data).execute()
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao criar solicitação: {result.error}")
            
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_usuarios(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Buscar solicitação entre dois usuários"""
        try:
            result = (self.db.table("adiciona")
                     .select("*")
                     .or_(f"and(usuario1.eq.{usuario1},usuario2.eq.{usuario2}),and(usuario1.eq.{usuario2},usuario2.eq.{usuario1})")
                     .single()
                     .execute())
            
            if not result.data:
                return {"success": False, "error": "Solicitação não encontrada"}
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_usuario1(self, usuario1: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar solicitações enviadas por um usuário"""
        try:
            query = (self.db.table("adiciona")
                    .select("*")
                    .eq("usuario1", usuario1)
                    .order("datahora", desc=True))
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_usuario2(self, usuario2: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar solicitações recebidas por um usuário"""
        try:
            query = (self.db.table("adiciona")
                    .select("*")
                    .eq("usuario2", usuario2)
                    .order("datahora", desc=True))
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def find_by_status(self, status: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Buscar solicitações por status"""
        try:
            query = (self.db.table("adiciona")
                    .select("*")
                    .eq("status", status)
                    .order("datahora", desc=True))
            
            if limit:
                query = query.limit(limit)
            
            result = query.execute()
            
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_status(self, usuario1: str, usuario2: str, status: str) -> Dict[str, Any]:
        """Atualizar status da solicitação"""
        try:
            result = (self.db.table("adiciona")
                     .update({"status": status})
                     .eq("usuario1", usuario1)
                     .eq("usuario2", usuario2)
                     .execute())
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao atualizar status: {result.error}")
            
            if not result.data:
                return {"success": False, "error": "Solicitação não encontrada"}
            
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete(self, usuario1: str, usuario2: str) -> Dict[str, Any]:
        """Deletar solicitação"""
        try:
            result = (self.db.table("adiciona")
                     .delete()
                     .eq("usuario1", usuario1)
                     .eq("usuario2", usuario2)
                     .execute())
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Erro ao deletar solicitação: {result.error}")
            
            return {"success": True, "message": "Solicitação deletada com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}
