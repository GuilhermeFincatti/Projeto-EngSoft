# Sistema de Coleção - ESALQ Explorer

## Visão Geral

O sistema de coleção permite que usuários colecionem cartas escaneando QRCodes espalhados pelo campus da ESALQ. Cada carta tem uma raridade e pode ser coletada múltiplas vezes.

## Endpoints da API

### Coleção do Usuário

#### `GET /api/minha-colecao`
Busca todas as cartas coletadas pelo usuário autenticado.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "qrcode": "QR001",
      "quantidade": 2,
      "carta": {
        "qrcode": "QR001",
        "raridade": "comum",
        "imagem": "https://example.com/sol.png",
        "audio": null,
        "localizacao": "Prédio Principal"
      }
    }
  ]
}
```

#### `POST /api/colecao/adicionar`
Adiciona uma carta à coleção do usuário.

**Request:**
```json
{
  "carta_id": "QR001",
  "quantidade": 1
}
```

#### `DELETE /api/colecao/remover`
Remove uma carta da coleção do usuário.

**Request:**
```json
{
  "carta_id": "QR001", 
  "quantidade": 1
}
```

#### `GET /api/colecao/estatisticas`
Busca estatísticas da coleção do usuário.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_cartas": 15,
    "cartas_unicas": 8,
    "por_raridade": {
      "comum": 6,
      "rara": 4,
      "épica": 3,
      "lendária": 2
    }
  }
}
```

#### `GET /api/colecao/verificar/{carta_id}`
Verifica se o usuário possui uma carta específica.

#### `DELETE /api/colecao/limpar`
Remove todas as cartas da coleção do usuário (irreversível).

## Como Configurar

### 1. Backend

1. Execute as migrações do banco de dados
2. Popule com cartas de exemplo:
```bash
cd BackEnd
python scripts/criar_cartas_exemplo.py
```

### 2. Frontend

O frontend está configurado para usar a API automaticamente. As principais funcionalidades:

- **Carregamento automático**: Cartas são carregadas do servidor com fallback local
- **Sincronização**: Coleção sincronizada entre servidor e dispositivo
- **Pull-to-refresh**: Puxe para baixo na tela de coleção para atualizar

## Fluxo de Uso

1. **Usuário escaneia QRCode** → App detecta o código
2. **App chama API** → `POST /api/colecao/adicionar`
3. **Carta é adicionada** → Contador do usuário é atualizado
4. **Tela de coleção** → Mostra nova carta coletada

## Estrutura do Banco

### Tabela `carta`
```sql
CREATE TABLE Carta (
    QRCode VARCHAR PRIMARY KEY,
    Raridade VARCHAR,
    Imagem TEXT,
    Audio TEXT,
    Localizacao TEXT
);
```

### Tabela `coleta`
```sql
CREATE TABLE Coleta (
    Usuario VARCHAR REFERENCES Usuario(Nickname),
    QRCode VARCHAR REFERENCES Carta(QRCode),
    Quantidade INT,
    PRIMARY KEY (Usuario, QRCode)
);
```

## Tipos de Raridade

- **comum**: Cartas básicas, fáceis de encontrar
- **incomum**: Cartas um pouco mais raras
- **rara**: Cartas difíceis de encontrar
- **épica**: Cartas muito raras
- **lendária**: Cartas extremamente raras

## Funcionalidades Futuras

- [ ] Sistema de troca entre usuários
- [ ] Cartas com efeitos especiais
- [ ] Missões para coletar cartas específicas
- [ ] Rankings de colecionadores
- [ ] Cartas temporárias/sazonais

## Troubleshooting

### Erro "Carta não encontrada"
- Verifique se a carta existe na tabela `carta`
- Execute o script `criar_cartas_exemplo.py`

### Erro de autenticação
- Certifique-se de que o token está sendo enviado
- Verifique se o usuário está logado

### Dados não sincronizando
- Verifique a conexão com o servidor
- Use pull-to-refresh na tela de coleção
