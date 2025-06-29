"""
Gerador de QR Codes para Cartas - Versão HTML
Este script gera uma página HTML com QR codes que podem ser impressos
"""

def gerar_html_qrcodes():
    """Gerar página HTML com QR codes das cartas"""
    
    cartas = [
        {"qrcode": "QR001", "nome": "Carta do Sol", "raridade": "comum", "cor": "#4CAF50"},
        {"qrcode": "QR002", "nome": "Carta da Lua", "raridade": "rara", "cor": "#FFD700"},
        {"qrcode": "QR003", "nome": "Carta de Mercúrio", "raridade": "comum", "cor": "#4CAF50"},
        {"qrcode": "QR004", "nome": "Carta de Vênus", "raridade": "incomum", "cor": "#FF9800"},
        {"qrcode": "QR005", "nome": "Carta da Terra", "raridade": "rara", "cor": "#FFD700"},
        {"qrcode": "QR006", "nome": "Carta de Marte", "raridade": "incomum", "cor": "#FF9800"},
        {"qrcode": "QR007", "nome": "Carta de Júpiter", "raridade": "lendária", "cor": "#FF5722"},
        {"qrcode": "QR008", "nome": "Carta de Saturno", "raridade": "lendária", "cor": "#FF5722"},
        {"qrcode": "QR009", "nome": "Carta de Urano", "raridade": "épica", "cor": "#9C27B0"},
        {"qrcode": "QR010", "nome": "Carta de Netuno", "raridade": "épica", "cor": "#9C27B0"},
        {"qrcode": "QR011", "nome": "Carta de Plutão", "raridade": "rara", "cor": "#FFD700"}
    ]
    
    html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Codes - ESALQ Explorer</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .carta {
            background: white;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 3px solid;
        }
        .qr-code {
            width: 200px;
            height: 200px;
            margin: 15px auto;
            display: block;
        }
        .nome {
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
            color: #333;
        }
        .codigo {
            font-size: 16px;
            color: #666;
            margin: 5px 0;
        }
        .raridade {
            font-size: 14px;
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            display: inline-block;
            margin: 10px 0;
            font-weight: bold;
            text-transform: uppercase;
        }
        .titulo {
            text-align: center;
            color: #2e7d32;
            font-size: 32px;
            margin-bottom: 30px;
        }
        .instrucoes {
            text-align: center;
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        @media print {
            body { margin: 0; }
            .instrucoes { display: none; }
            .carta { break-inside: avoid; }
        }
    </style>
</head>
<body>
    <h1 class="titulo">🎴 QR Codes - ESALQ Explorer</h1>
    
    <div class="instrucoes">
        <h3>📱 Como usar:</h3>
        <p>1. Imprima esta página</p>
        <p>2. Corte os QR codes</p>
        <p>3. Cole-os em locais do campus</p>
        <p>4. Use o app para escaneá-los e coletar as cartas!</p>
    </div>
    
    <div class="container">
"""
    
    for carta in cartas:
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={carta['qrcode']}"
        
        html_content += f"""
        <div class="carta" style="border-color: {carta['cor']};">
            <img src="{qr_url}" alt="QR Code {carta['qrcode']}" class="qr-code">
            <div class="nome">{carta['nome']}</div>
            <div class="codigo">{carta['qrcode']}</div>
            <div class="raridade" style="background-color: {carta['cor']};">
                {carta['raridade']}
            </div>
        </div>
        """
    
    html_content += """
    </div>
    
    <script>
        // Auto-print quando a página carregar (opcional)
        // window.onload = function() { window.print(); }
    </script>
</body>
</html>
"""
    
    # Salvar arquivo HTML
    output_path = "../../QRCodes/cartas_qrcodes.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Página HTML gerada: {output_path}")
    print("🖨️  Abra o arquivo no navegador e imprima para usar os QR codes!")
    
    return output_path

if __name__ == "__main__":
    gerar_html_qrcodes()
