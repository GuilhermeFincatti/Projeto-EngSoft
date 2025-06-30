# ESALQ Explorer 🎮🌱

Um jogo de cartas colecionáveis educativo desenvolvido para explorar o campus da ESALQ (Escola Superior de Agricultura "Luiz de Queiroz"). Os jogadores podem colecionar cartas escaneando QR codes espalhados pelo campus, completar missões e interagir com outros usuários através de um sistema de chat e trocas.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Configuração](#instalação-e-configuração)
  - [Backend (API)](#backend-api)
  - [Frontend (Mobile App)](#frontend-mobile-app)
  - [Banco de Dados (Supabase)](#banco-de-dados-supabase)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Endpoints](#api-endpoints)
- [Testes](#testes)
- [Contribuição](#contribuição)

## 🎯 Visão Geral

O ESALQ Explorer é um sistema gamificado que consiste em:

- **Backend API**: API RESTful desenvolvida em FastAPI
- **Frontend Mobile**: Aplicativo mobile desenvolvido em React Native com Expo
- **Banco de Dados**: Supabase (PostgreSQL)
- **Sistema de QR Codes**: Geração e leitura de QR codes para coleta de cartas

### Funcionalidades Principais

- 🃏 **Sistema de Cartas Colecionáveis**: Colecione cartas escaneando QR codes
- 🎯 **Missões**: Complete desafios e ganhe recompensas
- 🔄 **Sistema de Trocas**: Troque cartas com outros usuários
- 👥 **Sistema de Amizades**: Conecte-se com outros exploradores
- 📊 **Ranking**: Compete no sistema de pontuação
- 🗺️ **Mapa do Campus**: Navegue pelos locais das cartas

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **FastAPI** - Framework web moderno e rápido
- **Uvicorn** - Servidor ASGI
- **Supabase** - Backend as a Service
- **Pydantic** - Validação de dados
- **QRCode** - Geração de QR codes

### Frontend
- **React Native** - Framework para desenvolvimento mobile
- **Expo** - Plataforma para React Native
- **TypeScript** - Superset tipado do JavaScript
- **React Native Paper** - Biblioteca de componentes UI
- **React Native Maps** - Integração com mapas
- **Expo Camera** - Acesso à câmera do dispositivo

### Banco de Dados
- **Supabase** - PostgreSQL com recursos de tempo real
- **Autenticação** - Sistema de auth integrado

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

### Para o Backend:
- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/) (geralmente incluído com Python)

### Para o Frontend:
- [Node.js 18+](https://nodejs.org/)
- [npm](https://www.npmjs.com/) ou [yarn](https://yarnpkg.com/)
- [Expo CLI](https://docs.expo.dev/get-started/installation/)

### Para o Banco de Dados:
- Conta no [Supabase](https://supabase.com/)
- [Supabase CLI](https://supabase.com/docs/guides/cli) (opcional, para desenvolvimento local)

## 🚀 Instalação e Configuração

### Backend (API)

1. **Navegue para o diretório do backend:**
   ```powershell
   cd BackEnd
   ```

2. **Crie um ambiente virtual Python:**
   ```powershell
   python -m venv venv
   ```

3. **Ative o ambiente virtual:**
   ```powershell
   # No Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # No Windows CMD
   venv\Scripts\activate.bat
   ```

4. **Instale as dependências:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Configure as variáveis de ambiente:**
   
   Crie um arquivo `.env` no diretório `BackEnd` com as seguintes configurações:
   ```env
   SUPABASE_URL=sua_url_do_supabase
   SUPABASE_KEY=sua_chave_do_supabase
   SUPABASE_SERVICE_KEY=sua_service_key_do_supabase
   ```

### Frontend (Mobile App)

1. **Navegue para o diretório do frontend:**
   ```powershell
   cd FrontEnd\ESALQ_Explorer
   ```

2. **Instale as dependências:**
   ```powershell
   npm install
   # ou
   yarn install
   ```

3. **Configure as variáveis de ambiente:**
   
   Crie um arquivo `.env` no diretório `FrontEnd/ESALQ_Explorer` com:
   ```env
   EXPO_PUBLIC_API_URL=http://localhost:8000
   EXPO_PUBLIC_SUPABASE_URL=sua_url_do_supabase
   EXPO_PUBLIC_SUPABASE_ANON_KEY=sua_chave_publica_do_supabase
   ```

### Banco de Dados (Supabase)

1. **Configure o projeto Supabase:**
   
   Se você quiser rodar localmente com Supabase CLI:
   ```powershell
   cd supabase
   supabase start
   ```

2. **Execute as migrações:**
   ```powershell
   supabase db reset
   ```

   Ou se estiver usando Supabase na nuvem, execute as migrações através do dashboard do Supabase.

## 🏃‍♂️ Como Executar

### 1. Iniciar o Backend

```powershell
cd BackEnd
.\venv\Scripts\Activate.ps1  # Ative o ambiente virtual
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`
Documentação da API: `http://localhost:8000/docs`
### 2. Ajuste o arquivo do backendurl

Troque o arquivo FrontEnd/ESALQ_Explorer/constants/api.js com o seu endereço de IP local. É possivel descobrir através do comando `ipconfig`

### 3. Iniciar o Frontend

Em um novo terminal:

```powershell
cd FrontEnd\ESALQ_Explorer
npm start
# ou
expo start
```

Opções para executar o app:
- **Android**: `npm run android` ou pressione `a` no terminal
- **iOS**: `npm run ios` ou pressione `i` no terminal  
- **Web**: `npm run web` ou pressione `w` no terminal


## 📁 Estrutura do Projeto

```
Projeto-EngSoft/
├── BackEnd/                    # API FastAPI
│   ├── auth/                   # Módulos de autenticação
│   ├── config/                 # Configurações do banco
│   ├── controllers/            # Lógica de negócio
│   ├── models/                 # Modelos de dados
│   ├── routes/                 # Rotas da API
│   ├── docs/                   # Documentação
│   ├── main.py                 # Arquivo principal da API
│   └── requirements.txt        # Dependências Python
├── FrontEnd/                   # Aplicativo Mobile
│   └── ESALQ_Explorer/
│       ├── app/                # Páginas e navegação
│       ├── components/         # Componentes reutilizáveis
│       ├── services/           # Serviços de API
│       └── package.json        # Dependências Node.js
├── QRCodes/                    # Geração de QR codes
├── supabase/                   # Configuração e migrações
│   ├── migrations/             # Scripts de migração
│   └── config.toml            # Configuração do Supabase
└── README.md                   # Este arquivo
```

## 🔌 API Endpoints

A API possui os seguintes módulos principais:

### Autenticação
- `POST /register` - Registrar novo usuário
- `POST /login` - Fazer login
- `POST /reset-password` - Resetar senha

### Usuários e Pessoas
- `GET /api/pessoas` - Listar pessoas
- `GET /api/usuarios` - Listar usuários

### Cartas e Coleção
- `GET /api/cartas` - Listar cartas disponíveis
- `GET /api/minha-colecao` - Ver coleção do usuário
- `POST /api/colecao/adicionar` - Adicionar carta à coleção

### Missões
- `GET /api/missoes` - Listar missões
- `GET /api/missoes-quantidade` - Missões por quantidade
- `GET /api/missoes-raridade` - Missões por raridade

### Chat e Mensagens
- `GET /api/chats` - Listar chats
- `POST /api/mensagens` - Enviar mensagem

### Amizades
- `GET /api/amizades` - Listar amizades
- `POST /api/amizades` - Solicitar amizade

Para documentação completa, acesse: `http://localhost:8000/docs`

## 🧪 Testes

Para executar os testes do backend:

```powershell
cd BackEnd
python -m pytest test_database.py -v
python -m pytest test_leaderboard.py -v
python -m pytest test_upload.py -v
python -m pytest test_users.py -v
```

## 🤝 Contribuição

1. **Fork o projeto**
2. **Crie uma branch para sua feature** (`git checkout -b feature/MinhaFeature`)
3. **Commit suas mudanças** (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push para a branch** (`git push origin feature/MinhaFeature`)
5. **Abra um Pull Request**

## 📝 Notas Importantes

- **Primeiro Uso**: Na primeira execução, certifique-se de que o banco de dados está configurado e as migrações foram executadas
- **Porta do Backend**: O backend roda na porta 8000 por padrão
- **Ambiente de Desenvolvimento**: Use o ambiente virtual Python para evitar conflitos de dependências
- **QR Codes**: Os QR codes devem estar espalhados fisicamente pelo campus para a experiência completa

## 🐛 Solução de Problemas

### Backend não inicia
- Verifique se o ambiente virtual está ativo
- Confirme se todas as dependências estão instaladas
- Verifique as variáveis de ambiente no arquivo `.env`

### Frontend não conecta com o backend
- Certifique-se de que o backend está rodando na porta 8000
- Verifique a configuração da `EXPO_PUBLIC_API_URL`

### Problemas com Supabase
- Confirme suas credenciais no arquivo `.env`
- Verifique se as migrações foram executadas corretamente

---

**Desenvolvido por**

| Nome  | NUSP |
|-------|--------|
| Johnatas  | 13676388      |
| Aruan | 12609731      |
| Guilherme | 13676986      |
| Marcelo | 13676965      |
| Giovanni | 13695341      |
| Pedro | 13676919      |

--------------------