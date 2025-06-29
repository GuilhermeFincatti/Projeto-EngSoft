# BackEnd/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from auth.supabase_client import supabase
from auth.register_user import register_user
from auth.login_user import login_user
from auth.reset_password import reset_password

# Import new routes
from routes.pessoa_routes import router as pessoa_router
from routes.carta_routes import router as carta_router
from routes.mensagem_routes import router as mensagem_router
from routes.usuario_routes import router as usuario_router
from routes.adiciona_routes import router as adiciona_router
from routes.chat_routes import router as chat_router
from routes.missaoqtd_routes import router as missaoqtd_router
from routes.cartarara_routes import router as cartarara_router
from routes.educador_routes import router as educador_router
from routes.missao_routes import router as missao_router
from routes.missaoraridade_routes import router as missaoraridade_router
from routes.participaquantidade_routes import router as participaquantidade_router
from routes.participararidade_routes import router as participararidade_router
from routes.colecao_routes import router as colecao_router
from routes.amizade_routes import router as amizade_router

app = FastAPI(
    title="ESALQ Explorer API", 
    version="1.0.0",
    description="""
    API para o sistema ESALQ Explorer - um jogo de cartas colecionáveis educativo.
    
    ## Autenticação
    
    Todas as rotas protegidas requerem autenticação via Bearer Token.
    Para obter um token, faça login através do endpoint `/login`.
    
    ## Recursos Principais
    
    * **Pessoas**: Gerenciamento de usuários e educadores
    * **Cartas**: Gerenciamento das cartas colecionáveis
    
    ## Como usar
    
    1. Registre-se usando `/register`
    2. Faça login usando `/login` para obter o token
    3. Use o token no header Authorization: `Bearer <seu_token>`
    """,
    contact={
        "name": "ESALQ Explorer Team",
        "email": "contato@esalqexplorer.com",
    }
)

# Security scheme
security = HTTPBearer()

# Libera CORS para testes locais com o front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja isso
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pessoa_router, prefix="/api")
app.include_router(carta_router, prefix="/api")
app.include_router(mensagem_router, prefix="/api")
app.include_router(usuario_router, prefix="/api")
app.include_router(adiciona_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(missaoqtd_router, prefix="/api")
app.include_router(cartarara_router, prefix="/api")
app.include_router(educador_router, prefix="/api")
app.include_router(missao_router, prefix="/api")
app.include_router(missaoraridade_router, prefix="/api")
app.include_router(participaquantidade_router, prefix="/api")
app.include_router(participararidade_router, prefix="/api")
app.include_router(colecao_router)
app.include_router(amizade_router, prefix="/api")

class RegisterRequest(BaseModel):
    nickname: str
    email: str
    password: str
    tipo: str = "usuario"

class LoginRequest(BaseModel):
    nickname: str
    password: str

class ResetRequest(BaseModel):
    nickname: str

@app.get("/")
def root():
    return {"message": "API ESALQ Explorer rodando!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "message": "API funcionando corretamente"
    }

@app.post("/register")
def register(data: RegisterRequest):
    try:
        user = register_user(data.nickname, data.email, data.password, data.tipo)
        return {"message": "Usuário registrado com sucesso", "user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
def login(data: LoginRequest):
    try:
        session_response = login_user(data.nickname, data.password)
        return {
            "access_token": session_response.session.access_token,
            "user": session_response.user
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/reset-password")
def reset(data: ResetRequest):
    try:
        result = reset_password(data.nickname)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
