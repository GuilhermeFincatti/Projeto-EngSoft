# 📱 Sistema de QR Codes - ESALQ Explorer

## 🎯 Visão Geral

O sistema de QR codes permite que usuários colecionem cartas escaneando códigos espalhados pelo campus. Inclui scanner de câmera integrado e gerador de QR codes para teste.

## 📦 Dependências Necessárias

### Backend
```bash
pip install qrcode[pil]
```

### Frontend
```bash
npm install expo-camera react-native-qrcode-svg
```

## 🚀 Como Configurar

### 1. Backend - Popule o Banco

```bash
cd BackEnd
python scripts/criar_cartas_exemplo.py
```

### 2. Gere QR Codes para Teste

**Opção 1: HTML (Recomendado)**
```bash
python scripts/gerar_qrcodes_html.py
```
- Gera arquivo `QRCodes/cartas_qrcodes.html`
- Abra no navegador e imprima

**Opção 2: Python (Requer qrcode)**
```bash
python scripts/gerar_qrcodes.py
```

### 3. Frontend - Teste no App

1. **Inicie o app** e faça login
2. **Toque no botão 🧪** (canto superior direito) 
3. **Visualize QR codes** na tela de teste
4. **Toque "Abrir Scanner"** para testar
5. **Escaneie qualquer QR code** da tela

## 📱 Funcionalidades

### Scanner de Câmera (`/camera`)

- **Permissões automáticas**: Solicita acesso à câmera
- **Interface intuitiva**: Frame de escaneamento visual
- **Detecção rápida**: Reconhece QR codes instantaneamente  
- **Feedback visual**: Overlay e instruções claras
- **Tratamento de erros**: Mensagens amigáveis
- **Integração com API**: Adiciona cartas automaticamente

### Tela de Teste (`/test-qr`)

- **QR codes visuais**: Todos os códigos de teste em uma tela
- **Acesso rápido**: Botão direto para o scanner
- **Informações das cartas**: Nome, código e raridade
- **Design responsivo**: Adaptado para diferentes telas

### Fluxo de Coleta

```
1. Usuário abre scanner → 2. Escaneia QR code → 3. API adiciona carta → 4. Feedback de sucesso
```

## 🎨 QR Codes Disponíveis

| Código | Nome | Raridade | Cor |
|--------|------|----------|-----|
| QR001 | Carta do Sol | Comum | Verde |
| QR002 | Carta da Lua | Rara | Dourado |
| QR003 | Carta de Mercúrio | Comum | Verde |
| QR004 | Carta de Vênus | Incomum | Laranja |
| QR005 | Carta da Terra | Rara | Dourado |
| QR006 | Carta de Marte | Incomum | Laranja |
| QR007 | Carta de Júpiter | Lendária | Vermelho |
| QR008 | Carta de Saturno | Lendária | Vermelho |
| QR009 | Carta de Urano | Épica | Roxo |
| QR010 | Carta de Netuno | Épica | Roxo |
| QR011 | Carta de Plutão | Rara | Dourado |

## 🔧 Configuração de Permissões

### Android (`android/app/src/main/AndroidManifest.xml`)
```xml
<uses-permission android:name="android.permission.CAMERA" />
```

### iOS (`ios/YourApp/Info.plist`)
```xml
<key>NSCameraUsageDescription</key>
<string>Este app precisa da câmera para escanear QR codes das cartas</string>
```

## 🎯 API Endpoints Utilizados

- `POST /api/colecao/adicionar` - Adiciona carta coletada
- `GET /api/minha-colecao` - Lista cartas do usuário
- `GET /cartas` - Lista todas as cartas disponíveis

## 🐛 Troubleshooting

### Câmera não funciona
1. Verifique permissões no dispositivo
2. Teste em dispositivo físico (não funciona no simulador)
3. Certifique-se de que `expo-camera` está instalado

### QR code não reconhecido
1. Verifique se a carta existe no banco de dados
2. Execute `criar_cartas_exemplo.py`
3. Teste com boa iluminação

### Erro de API
1. Verifique se o backend está rodando
2. Confirme se o usuário está logado
3. Teste conectividade de rede

## 🎮 Como Testar

### Teste Rápido
1. Abra o app → Login
2. Toque 🧪 → "Abrir Scanner" 
3. Escaneie QR da tela de teste
4. Verifique coleção

### Teste Completo
1. Gere QR codes HTML
2. Imprima e cole no campus
3. Use app para escanear QR físicos
4. Verifique persistência no banco

## 📈 Próximas Funcionalidades

- [ ] Scanner batch (múltiplos QR codes)
- [ ] QR codes temporários/eventos
- [ ] Análise de localização GPS
- [ ] Histórico de escaneamentos
- [ ] QR codes com recompensas especiais

## 🎉 Conclusão

O sistema está **100% funcional** e pronto para uso em produção! Os usuários podem facilmente coletar cartas escaneando QR codes, com uma experiência fluida e intuitiva.
