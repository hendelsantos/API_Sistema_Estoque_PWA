#!/usr/bin/env python
"""
Script para criar dados de exemplo no sistema de gestão de estoque
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/home/hendel/Documentos/API/GestaoEstoques')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_estoque.settings')
django.setup()

from estoque.models import Categoria, Fornecedor, Produto, MovimentacaoEstoque
from django.contrib.auth.models import User

def criar_dados_exemplo():
    print("Criando dados de exemplo...")
    
    # Criar categorias
    categorias = [
        {"nome": "Eletrônicos", "descricao": "Equipamentos eletrônicos e acessórios"},
        {"nome": "Ferramentas", "descricao": "Ferramentas manuais e elétricas"},
        {"nome": "Material de Escritório", "descricao": "Papelaria e material de escritório"},
        {"nome": "Limpeza", "descricao": "Produtos de limpeza e higiene"},
        {"nome": "Informática", "descricao": "Equipamentos e acessórios de informática"},
    ]
    
    for cat_data in categorias:
        categoria, created = Categoria.objects.get_or_create(
            nome=cat_data["nome"],
            defaults={"descricao": cat_data["descricao"]}
        )
        if created:
            print(f"✓ Categoria criada: {categoria.nome}")
    
    # Criar fornecedores
    fornecedores = [
        {
            "nome": "TechMais Distribuidora",
            "cnpj": "12.345.678/0001-90",
            "telefone": "(11) 98765-4321",
            "email": "vendas@techmais.com.br",
            "endereco": "Rua das Tecnologias, 123 - São Paulo, SP"
        },
        {
            "nome": "Ferramentas & Cia",
            "cnpj": "98.765.432/0001-10",
            "telefone": "(11) 91234-5678",
            "email": "contato@ferramentasecia.com.br",
            "endereco": "Av. Industrial, 456 - São Paulo, SP"
        },
        {
            "nome": "OfficeMax Ltda",
            "cnpj": "11.222.333/0001-44",
            "telefone": "(11) 95555-1234",
            "email": "vendas@officemax.com.br",
            "endereco": "Rua do Comércio, 789 - São Paulo, SP"
        }
    ]
    
    for forn_data in fornecedores:
        fornecedor, created = Fornecedor.objects.get_or_create(
            cnpj=forn_data["cnpj"],
            defaults=forn_data
        )
        if created:
            print(f"✓ Fornecedor criado: {fornecedor.nome}")
    
    # Criar produtos
    produtos = [
        {
            "codigo": "MOUSE001",
            "nome": "Mouse Óptico USB",
            "descricao": "Mouse óptico com conexão USB, ergonômico",
            "categoria": "Informática",
            "fornecedor": "TechMais Distribuidora",
            "quantidade_atual": 25,
            "quantidade_minima": 10,
            "preco_custo": 15.90,
            "preco_venda": 29.90,
            "unidade_medida": "UN",
            "localizacao": "Estante A, Prateleira 1"
        },
        {
            "codigo": "TECLADO001",
            "nome": "Teclado USB ABNT2",
            "descricao": "Teclado padrão ABNT2 com conexão USB",
            "categoria": "Informática",
            "fornecedor": "TechMais Distribuidora",
            "quantidade_atual": 8,
            "quantidade_minima": 15,
            "preco_custo": 45.00,
            "preco_venda": 79.90,
            "unidade_medida": "UN",
            "localizacao": "Estante A, Prateleira 2"
        },
        {
            "codigo": "FURADEIRA001",
            "nome": "Furadeira de Impacto 500W",
            "descricao": "Furadeira de impacto com potência de 500W",
            "categoria": "Ferramentas",
            "fornecedor": "Ferramentas & Cia",
            "quantidade_atual": 5,
            "quantidade_minima": 3,
            "preco_custo": 120.00,
            "preco_venda": 199.90,
            "unidade_medida": "UN",
            "localizacao": "Estante B, Prateleira 1"
        },
        {
            "codigo": "PAPEL001",
            "nome": "Papel A4 75g (Resma)",
            "descricao": "Resma de papel A4 com 500 folhas, 75g/m²",
            "categoria": "Material de Escritório",
            "fornecedor": "OfficeMax Ltda",
            "quantidade_atual": 50,
            "quantidade_minima": 20,
            "preco_custo": 18.50,
            "preco_venda": 32.90,
            "unidade_medida": "UN",
            "localizacao": "Estante C, Prateleira 1"
        },
        {
            "codigo": "CANETA001",
            "nome": "Caneta Esferográfica Azul",
            "descricao": "Caneta esferográfica azul, ponta média",
            "categoria": "Material de Escritório",
            "fornecedor": "OfficeMax Ltda",
            "quantidade_atual": 2,
            "quantidade_minima": 50,
            "preco_custo": 1.20,
            "preco_venda": 2.50,
            "unidade_medida": "UN",
            "localizacao": "Estante C, Gaveta 1"
        },
        {
            "codigo": "DETER001",
            "nome": "Detergente Neutro 500ml",
            "descricao": "Detergente neutro multiuso 500ml",
            "categoria": "Limpeza",
            "quantidade_atual": 12,
            "quantidade_minima": 8,
            "preco_custo": 3.50,
            "preco_venda": 6.90,
            "unidade_medida": "UN",
            "localizacao": "Estante D, Prateleira 1"
        }
    ]
    
    for prod_data in produtos:
        try:
            categoria = Categoria.objects.get(nome=prod_data["categoria"])
            fornecedor = None
            if prod_data.get("fornecedor"):
                fornecedor = Fornecedor.objects.get(nome=prod_data["fornecedor"])
            
            produto, created = Produto.objects.get_or_create(
                codigo=prod_data["codigo"],
                defaults={
                    "nome": prod_data["nome"],
                    "descricao": prod_data["descricao"],
                    "categoria": categoria,
                    "fornecedor": fornecedor,
                    "quantidade_atual": prod_data["quantidade_atual"],
                    "quantidade_minima": prod_data["quantidade_minima"],
                    "preco_custo": prod_data["preco_custo"],
                    "preco_venda": prod_data["preco_venda"],
                    "unidade_medida": prod_data["unidade_medida"],
                    "localizacao": prod_data["localizacao"]
                }
            )
            if created:
                print(f"✓ Produto criado: {produto.nome}")
        except Exception as e:
            print(f"✗ Erro ao criar produto {prod_data['nome']}: {e}")
    
    print("\n🎉 Dados de exemplo criados com sucesso!")
    print(f"📦 {Categoria.objects.count()} categorias")
    print(f"🏢 {Fornecedor.objects.count()} fornecedores")
    print(f"📦 {Produto.objects.count()} produtos")
    
    # Produtos com estoque baixo
    produtos_baixo = Produto.objects.filter(quantidade_atual__lte=django.db.models.F('quantidade_minima'))
    if produtos_baixo.exists():
        print(f"\n⚠️  Produtos com estoque baixo:")
        for p in produtos_baixo:
            print(f"   - {p.nome}: {p.quantidade_atual} (mín: {p.quantidade_minima})")

if __name__ == "__main__":
    criar_dados_exemplo()
