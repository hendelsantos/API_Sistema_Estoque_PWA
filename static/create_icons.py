from PIL import Image, ImageDraw, ImageFont
import os

def create_simple_icon(size, filepath):
    """Cria um ícone PNG simples"""
    # Criar imagem com fundo azul
    img = Image.new('RGB', (size, size), '#0d6efd')
    draw = ImageDraw.Draw(img)
    
    # Desenhar um quadrado branco no centro (representando uma caixa)
    margin = size // 4
    box_coords = [margin, margin, size - margin, size - margin]
    draw.rectangle(box_coords, fill='white', outline='#e9ecef', width=2)
    
    # Adicionar algumas linhas para simular estoque
    if size >= 32:
        # Linha horizontal
        y_mid = size // 2
        draw.line([(margin, y_mid), (size - margin, y_mid)], fill='#e9ecef', width=2)
        
        # Linha vertical
        x_mid = size // 2
        draw.line([(x_mid, margin), (x_mid, size - margin)], fill='#e9ecef', width=2)
    
    # Adicionar mini QR code se o ícone for grande o suficiente
    if size >= 48:
        qr_size = size // 6
        qr_x = margin + qr_size // 2
        qr_y = margin + qr_size // 2
        
        # QR code simplificado (alguns quadrados)
        for i in range(0, qr_size, 3):
            for j in range(0, qr_size, 3):
                if (i + j) % 6 == 0:
                    draw.rectangle([qr_x + i, qr_y + j, qr_x + i + 2, qr_y + j + 2], fill='#0d6efd')
    
    # Salvar arquivo
    img.save(filepath, 'PNG')
    print(f"Criado: {filepath}")

def create_favicon():
    """Cria um favicon.ico"""
    sizes = [16, 32, 48]
    images = []
    
    for size in sizes:
        img = Image.new('RGB', (size, size), '#0d6efd')
        draw = ImageDraw.Draw(img)
        
        # Desenhar 'E' simplificado
        margin = size // 4
        thickness = max(1, size // 8)
        
        # Letra E
        draw.rectangle([margin, margin, margin + thickness, size - margin], fill='white')
        draw.rectangle([margin, margin, size - margin - thickness, margin + thickness], fill='white')
        draw.rectangle([margin, size//2 - thickness//2, size - margin - thickness//2, size//2 + thickness//2], fill='white')
        draw.rectangle([margin, size - margin - thickness, size - margin - thickness, size - margin], fill='white')
        
        images.append(img)
    
    # Salvar como ICO
    images[0].save('/home/hendel/Documentos/API/GestaoEstoques/static/favicon.ico', 
                   format='ICO', sizes=[(16,16), (32,32), (48,48)])
    print("Criado: favicon.ico")

if __name__ == "__main__":
    # Tamanhos necessários
    sizes = [16, 32, 48, 72, 96, 128, 144, 152, 180, 192, 384, 512]
    base_path = "/home/hendel/Documentos/API/GestaoEstoques/static/icons"
    
    print("Gerando ícones PNG...")
    
    for size in sizes:
        filepath = f"{base_path}/icon-{size}x{size}.png"
        create_simple_icon(size, filepath)
    
    # Criar favicon
    create_favicon()
    
    print("\n✅ Todos os ícones foram gerados com sucesso!")
    print("Os ícones estão prontos para uso com a PWA.")
