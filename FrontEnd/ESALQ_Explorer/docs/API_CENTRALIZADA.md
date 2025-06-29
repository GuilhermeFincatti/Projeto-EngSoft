# API Centralizada - Documentação

## Visão Geral

O serviço de API centralizado (`services/api.js`) gerencia todas as requisições para o backend, incluindo:
- Gerenciamento automático de tokens de acesso
- Tratamento padronizado de erros
- Refresh automático de dados
- Fallback para dados locais

## Como usar

### 1. Import do serviço

```javascript
import { apiService, ApiError, NetworkError } from '../services/api'
```

### 2. Autenticação

```javascript
// Login (salva automaticamente o token)
try {
  await apiService.login(nickname, password)
  // Usuário logado com sucesso
} catch (error) {
  // Trata erro de login
}

// Logout (limpa token e dados)
await apiService.logout()

// Verificar se token é válido
const isValid = await apiService.validateToken()
```

### 3. Requisições de Cartas

```javascript
// Buscar todas as cartas disponíveis
const cartas = await apiService.getCartas()

// Buscar carta específica
const carta = await apiService.getCarta(cartaId)

// Buscar coleção do usuário
const minhaColecao = await apiService.getMinhaColecao()

// Adicionar carta à coleção
await apiService.adicionarCartaColecao(cartaId)
```

### 4. Tratamento de Erros

```javascript
try {
  const data = await apiService.getCartas()
} catch (error) {
  if (error instanceof ApiError) {
    // Erro da API (400, 401, 500, etc.)
    Alert.alert('Erro', error.getUserMessage())
  } else if (error instanceof NetworkError) {
    // Erro de rede/conectividade
    Alert.alert('Erro', error.getUserMessage())
  } else {
    // Erro desconhecido
    Alert.alert('Erro', 'Erro inesperado')
  }
}
```

## Estrutura do Token

O token de acesso é automaticamente:
- Salvo no AsyncStorage após login bem-sucedido
- Incluído em todas as requisições subsequentes
- Verificado para validade quando necessário
- Removido automaticamente em caso de erro 401

## Endpoints Esperados no Backend

### Autenticação
- `POST /login` - Login do usuário
  - Body: `{ nickname, password }`
  - Response: `{ access_token, ... }`

### Cartas
- `GET /api/cartas` - Lista todas as cartas
- `GET /api/cartas/{id}` - Detalhes de uma carta
- `GET /api/minha-colecao` - Coleção do usuário atual
- `POST /api/colecao/adicionar` - Adiciona carta à coleção
  - Body: `{ carta_id }`

### Validação
- `GET /api/me` - Dados do usuário atual (para validar token)

## Hooks Utilitários

### useAuth Hook

```javascript
import { useAuth } from '../hooks/useAuth'

const { isAuthenticated, user, loading, login, logout } = useAuth()

// Usar nos componentes para controlar estado de autenticação
```

## Componentes Auxiliares

### CartaCollectButton

```javascript
import CartaCollectButton from '../components/CartaCollectButton'

<CartaCollectButton 
  cartaId={carta.id} 
  onCartaColetada={(id) => {
    // Callback quando carta é coletada
  }} 
/>
```

## Fallbacks e Resiliência

- Se a API não estiver disponível, usa dados locais como fallback
- Dados são salvos no AsyncStorage como backup
- Requisições falham graciosamente sem quebrar a aplicação
- Mensagens de erro amigáveis para o usuário

## Configuração

Certifique-se de que `constants/api.js` tem a URL correta:

```javascript
export const BACKEND_URL = "http://SEU_IP:8000"
```

## Splash Screen

O aplicativo usa o logo do ESALQ Explorer como splash screen:
- Configurado em `app.json` para mostrar automaticamente
- Componente customizado `CustomSplashScreen` para animações
- Duração configurável no `_layout.jsx`

### Personalização da Splash Screen

Para alterar a duração da splash screen:
```javascript
// Em _layout.jsx
setTimeout(async () => {
  await SplashScreen.hideAsync();
}, 2000); // Altere para a duração desejada em ms
```
