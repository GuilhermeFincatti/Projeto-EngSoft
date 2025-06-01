# BackEnd/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from auth.supabase_client import supabase
from auth.register_user import register_user
from auth.login_user import login_user
from auth.reset_password import reset_password

app = FastAPI()

# Libera CORS para testes locais com o front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja isso
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {"message": "API Supabase rodando!"}

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
        session = login_user(data.nickname, data.password)
        return {"access_token": session.access_token, "user": session.user}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/reset-password")
def reset(data: ResetRequest):
    try:
        result = reset_password(data.nickname)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
