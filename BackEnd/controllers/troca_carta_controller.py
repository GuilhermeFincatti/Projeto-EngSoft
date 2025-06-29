from typing import Dict, Any
from models.troca_carta_model import TrocaCartaModel
from models.mensagem_model import MensagemModel

class TrocaCartaController:
    def __init__(self):
        self.troca_model = TrocaCartaModel()
        self.mensagem_model = MensagemModel()
    
    def propor_troca(self, solicitante: str, destinatario: str, 
                    carta_oferecida: str, carta_solicitada: str) -> Dict[str, Any]:
        """Propor uma troca de cartas"""
        try:
            # Criar solicitação de troca
            result = self.troca_model.criar_solicitacao_troca(
                solicitante, destinatario, carta_oferecida, carta_solicitada
            )
            
            if result["success"]:
                troca_id = result["data"]["id"]
                
                # Enviar mensagem sobre a troca
                texto_troca = f"🔄 Proposta de troca: Oferece {carta_oferecida} por {carta_solicitada}"
                self.mensagem_model.send_message(
                    remetente=solicitante,
                    destinatario=destinatario,
                    texto=texto_troca,
                    tipo="troca",
                    troca_id=troca_id
                )
                
                return {"success": True, "data": result["data"], "message": "Proposta de troca enviada!"}
            else:
                return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def responder_troca(self, troca_id: int, usuario: str, aceitar: bool) -> Dict[str, Any]:
        """Aceitar ou rejeitar uma troca"""
        try:
            if aceitar:
                result = self.troca_model.aceitar_troca(troca_id, usuario)
                if result["success"]:
                    # Enviar mensagem confirmando a troca
                    troca_info = self.troca_model.db.table("trocacarta").select("*").eq("id", troca_id).single().execute()
                    if troca_info.data:
                        solicitante = troca_info.data["solicitante"]
                        self.mensagem_model.send_message(
                            remetente=usuario,
                            destinatario=solicitante,
                            texto="✅ Troca aceita! As cartas foram trocadas com sucesso.",
                            tipo="troca",
                            troca_id=troca_id
                        )
            else:
                result = self.troca_model.rejeitar_troca(troca_id, usuario)
                if result["success"]:
                    # Enviar mensagem rejeitando a troca
                    troca_info = self.troca_model.db.table("trocacarta").select("*").eq("id", troca_id).single().execute()
                    if troca_info.data:
                        solicitante = troca_info.data["solicitante"]
                        self.mensagem_model.send_message(
                            remetente=usuario,
                            destinatario=solicitante,
                            texto="❌ Troca rejeitada.",
                            tipo="troca",
                            troca_id=troca_id
                        )
            
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def listar_trocas(self, usuario: str) -> Dict[str, Any]:
        """Listar trocas do usuário"""
        return self.troca_model.listar_trocas_usuario(usuario)
