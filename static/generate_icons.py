#!/usr/bin/env python3
"""
Script para gerar ícones PWA em diferentes tamanhos
Usa o SVG base para criar PNGs nos tamanhos necessários
"""

import os
from pathlib import Path

# Para uso futuro com bibliotecas como cairosvg ou wand
# Por enquanto, criamos placeholders HTML que o navegador pode renderizar

def create_html_icon_placeholder(size, output_path):
    """Cria um placeholder HTML que pode ser convertido para PNG"""
    html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            width: {size}px;
            height: {size}px;
            background: #0d6efd;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: Arial, sans-serif;
        }}
        .icon {{
            width: {size}px;
            height: {size}px;
            background: #0d6efd;
            border-radius: {size//6}px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .box {{
            width: {size*0.6}px;
            height: {size*0.45}px;
            background: white;
            border-radius: {size//20}px;
            border: 2px solid #e9ecef;
            position: relative;
        }}
        .qr {{
            position: absolute;
            left: {size*0.08}px;
            top: {size*0.08}px;
            width: {size*0.15}px;
            height: {size*0.15}px;
            background: #0d6efd;
            border-radius: 2px;
        }}
        .text {{
            position: absolute;
            bottom: {size*0.1}px;
            width: 100%;
            text-align: center;
            color: white;
            font-size: {size//14}px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="icon">
        <div class="box">
            <div class="qr"></div>
        </div>
        <div class="text">EA</div>
    </div>
</body>
</html>
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_favicon_ico():
    """Cria um favicon.ico simples usando dados base64"""
    # Dados de um favicon 16x16 simples em base64
    favicon_data = '''
AAABAAEAEBAAAAEACABoBQAAFgAAACgAAAAQAAAAIAAAAAEACAAAAAAAAAEAAAAAAAAAAAAAAAEAAAAAAAAAAAAA
/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAA
AP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8A
AAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/
AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA
/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAA
AP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8A
AAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/
AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA
/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAA
AP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8A
AAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/
AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA
/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAA
AP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8A
AAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/
AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA
/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAA
AP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8A
AAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/
AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA
/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAA
'''
    return favicon_data.strip()

if __name__ == "__main__":
    # Definir diretório base
    base_dir = Path(__file__).parent
    icons_dir = base_dir / "icons"
    
    # Criar diretório se não existir
    icons_dir.mkdir(exist_ok=True)
    
    # Tamanhos necessários para PWA
    sizes = [16, 32, 48, 72, 96, 128, 144, 152, 180, 192, 384, 512]
    
    print("Gerando placeholders de ícones...")
    
    for size in sizes:
        filename = f"icon-{size}x{size}.html"
        filepath = icons_dir / filename
        create_html_icon_placeholder(size, filepath)
        print(f"Criado: {filename}")
    
    print("\\nPara converter para PNG, você pode usar:")
    print("1. Screenshot das páginas HTML")
    print("2. Ferramentas online de conversão")
    print("3. Bibliotecas Python como cairosvg ou wand")
    print("\\nPor enquanto, use o SVG principal como fallback.")
