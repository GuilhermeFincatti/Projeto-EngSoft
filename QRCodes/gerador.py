import qrcode

# Lista de códigos das árvores
numeros = [1, 2]

for numero in numeros:
    img = qrcode.make(str(numero))
    img.save(f"qr_{numero}.png")
