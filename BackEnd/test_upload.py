import requests
import base64
import json

# URL do endpoint
url = "http://localhost:8000/api/usuarios/leaderboard"

# Criar uma imagem simples em base64 para teste (pequeno pixel GIF transparente)
# GIF de 1x1 pixel transparente
gif_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x04\x01\x00\x3b'
encoded_image = base64.b64encode(gif_data).decode('utf-8')

# Dados para enviar
data = {
    "photo_data": encoded_image
}

# Headers
headers = {
    "Content-Type": "application/json",
    # Removendo autenticação temporariamente para testar
}

try:
    response = requests.get(url,  headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Erro na requisição: {e}")
