import qrcode
import os
from pathlib import Path

def gerar_qrcodes_cartas():
    """Gerar QR codes para as cartas de exemplo"""
    
    # Lista das cartas de exemplo
    cartas = [
        {"qrcode": "QR001", "nome": "Carta do Sol", "raridade": "comum"},
        {"qrcode": "QR002", "nome": "Carta da Lua", "raridade": "rara"},
        {"qrcode": "QR003", "nome": "Carta de Mercúrio", "raridade": "comum"},
        {"qrcode": "QR004", "nome": "Carta de Vênus", "raridade": "incomum"},
        {"qrcode": "QR005", "nome": "Carta da Terra", "raridade": "rara"},
        {"qrcode": "QR006", "nome": "Carta de Marte", "raridade": "incomum"},
        {"qrcode": "QR007", "nome": "Carta de Júpiter", "raridade": "lendária"},
        {"qrcode": "QR008", "nome": "Carta de Saturno", "raridade": "lendária"},
        {"qrcode": "QR009", "nome": "Carta de Urano", "raridade": "épica"},
        {"qrcode": "QR010", "nome": "Carta de Netuno", "raridade": "épica"},
        {"qrcode": "QR011", "nome": "Carta de Plutão", "raridade": "rara"}
    ]
    
    # Criar diretório para os QR codes se não existir
    output_dir = Path("../../QRCodes/cartas")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🔄 Gerando QR codes das cartas...")
    
    for carta in cartas:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # O QR code contém apenas o código da carta
        qr.add_data(carta["qrcode"])
        qr.make(fit=True)
        
        # Criar imagem do QR code
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Salvar imagem
        filename = f"{carta['qrcode']}_{carta['raridade']}.png"
        filepath = output_dir / filename
        img.save(filepath)
        
        print(f"✅ {filename} - {carta['nome']} ({carta['raridade']})")
    
    print(f"\n✨ {len(cartas)} QR codes gerados em: {output_dir.absolute()}")
    print("\n📱 Agora você pode imprimir estes QR codes e testá-los no app!")

def gerar_qrcode_individual(codigo, nome="Carta Teste"):
    """Gerar um QR code individual"""
    output_dir = Path("../../QRCodes/cartas")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(codigo)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"{codigo}_teste.png"
    filepath = output_dir / filename
    img.save(filepath)
    
    print(f"✅ QR code gerado: {filename}")
    return filepath

if __name__ == "__main__":
    gerar_qrcodes_cartas()
