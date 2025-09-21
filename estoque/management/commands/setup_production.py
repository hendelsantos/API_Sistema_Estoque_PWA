from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from estoque.models import Categoria, Fornecedor, Produto


class Command(BaseCommand):
    help = 'Configura dados iniciais para produção no Railway'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Configurando aplicação para produção...')
        )

        # Criar superusuário
        self.create_admin_user()
        
        # Criar usuário de teste
        self.create_test_user()
        
        # Criar dados de exemplo
        self.create_sample_data()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Configuração concluída com sucesso!')
        )
        
        self.stdout.write('\n📋 Credenciais de acesso:')
        self.stdout.write('👤 Admin: admin / admin123')
        self.stdout.write('👤 User: user / user123')

    def create_admin_user(self):
        """Cria usuário admin"""
        if User.objects.filter(username='admin').exists():
            self.stdout.write('✅ Superusuário admin já existe')
            return

        User.objects.create_superuser(
            username='admin',
            email='admin@gestaoestoque.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema'
        )
        self.stdout.write('✅ Superusuário admin criado')

    def create_test_user(self):
        """Cria usuário de teste"""
        if User.objects.filter(username='user').exists():
            self.stdout.write('✅ Usuário de teste já existe')
            return

        User.objects.create_user(
            username='user',
            email='user@gestaoestoque.com',
            password='user123',
            first_name='Usuário',
            last_name='Teste'
        )
        self.stdout.write('✅ Usuário de teste criado')

    def create_sample_data(self):
        """Cria dados de exemplo"""
        # Categorias
        categorias_data = [
            'Eletrônicos',
            'Informática', 
            'Casa e Jardim',
            'Roupas e Acessórios',
            'Livros e Papelaria'
        ]
        
        for nome in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nome=nome,
                defaults={'descricao': f'Categoria {nome}'}
            )
            if created:
                self.stdout.write(f'✅ Categoria criada: {nome}')

        # Fornecedores
        fornecedores_data = [
            ('TechSupply Ltda', 'tech@supply.com', '(11) 99999-1111'),
            ('InfoParts S/A', 'vendas@infoparts.com', '(11) 99999-2222'),
            ('Casa Moderna', 'contato@casamoderna.com', '(11) 99999-3333'),
        ]
        
        for nome, email, telefone in fornecedores_data:
            fornecedor, created = Fornecedor.objects.get_or_create(
                nome=nome,
                defaults={
                    'email': email,
                    'telefone': telefone,
                    'endereco': 'Endereço de exemplo'
                }
            )
            if created:
                self.stdout.write(f'✅ Fornecedor criado: {nome}')

        # Produtos de exemplo
        if not Produto.objects.exists():
            categoria_eletronicos = Categoria.objects.get(nome='Eletrônicos')
            categoria_informatica = Categoria.objects.get(nome='Informática')
            fornecedor = Fornecedor.objects.first()
            
            produtos_data = [
                {
                    'codigo': 'SM001',
                    'nome': 'Smartphone Samsung Galaxy',
                    'categoria': categoria_eletronicos,
                    'fornecedor': fornecedor,
                    'preco_custo': 800.00,
                    'preco_venda': 1200.00,
                    'quantidade_atual': 15,
                    'quantidade_minima': 5
                },
                {
                    'codigo': 'NB001',
                    'nome': 'Notebook Dell Inspiron',
                    'categoria': categoria_informatica,
                    'fornecedor': fornecedor,
                    'preco_custo': 2500.00,
                    'preco_venda': 3500.00,
                    'quantidade_atual': 8,
                    'quantidade_minima': 3
                },
                {
                    'codigo': 'MS001',
                    'nome': 'Mouse Wireless Logitech',
                    'categoria': categoria_informatica,
                    'fornecedor': fornecedor,
                    'preco_custo': 45.00,
                    'preco_venda': 89.90,
                    'quantidade_atual': 2,  # Estoque baixo
                    'quantidade_minima': 10
                }
            ]
            
            for produto_data in produtos_data:
                Produto.objects.create(**produto_data)
                self.stdout.write(f'✅ Produto criado: {produto_data["nome"]}')
        else:
            self.stdout.write('✅ Produtos de exemplo já existem')
