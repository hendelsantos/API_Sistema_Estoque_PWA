#!/usr/bin/env python
"""
Script para criar usuário admin no Railway
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_estoque.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Cria usuário admin se não existir"""
    try:
        # Verificar se já existe um superusuário
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superusuário já existe!")
            admin_user = User.objects.filter(is_superuser=True).first()
            print(f"   Username: {admin_user.username}")
            return
        
        # Criar superusuário
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@gestaoestoque.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema'
        )
        
        print("✅ Superusuário criado com sucesso!")
        print(f"   Username: {admin_user.username}")
        print(f"   Password: admin123")
        print(f"   Email: {admin_user.email}")
        
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")

def create_test_user():
    """Cria usuário de teste se não existir"""
    try:
        if User.objects.filter(username='user').exists():
            print("✅ Usuário de teste já existe!")
            return
        
        test_user = User.objects.create_user(
            username='user',
            email='user@gestaoestoque.com', 
            password='user123',
            first_name='Usuário',
            last_name='Teste'
        )
        
        print("✅ Usuário de teste criado!")
        print(f"   Username: {test_user.username}")
        print(f"   Password: user123")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário de teste: {e}")

if __name__ == '__main__':
    print("🚀 Criando usuários do sistema...")
    create_admin_user()
    create_test_user()
    print("\n📋 Usuários disponíveis:")
    print("1. admin/admin123 (superusuário)")
    print("2. user/user123 (usuário comum)")
    print("\n✅ Script executado com sucesso!")
