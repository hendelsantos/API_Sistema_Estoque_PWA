from django.core.management.base import BaseCommand
from estoque.models import Categoria, Produto


class Command(BaseCommand):
    help = 'Gerencia apenas as categorias NLAG e ERSA'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpar-outras',
            action='store_true',
            help='Remove todas as categorias exceto NLAG e ERSA (apenas as vazias)',
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='Mostra status das categorias NLAG e ERSA',
        )

    def handle(self, *args, **options):
        self.stdout.write('🏷️ GERENCIADOR DE CATEGORIAS - NLAG e ERSA')
        self.stdout.write('=' * 50)

        # Garantir que NLAG e ERSA existem
        self.criar_categorias_principais()

        if options['status']:
            self.mostrar_status()
        elif options['limpar_outras']:
            self.limpar_outras_categorias()
        else:
            self.mostrar_menu()

    def criar_categorias_principais(self):
        """Cria as categorias NLAG e ERSA se não existirem"""
        categorias_data = [
            {
                'nome': 'NLAG',
                'descricao': 'Categoria NLAG - Produtos específicos'
            },
            {
                'nome': 'ERSA',
                'descricao': 'Categoria ERSA - Produtos específicos'
            }
        ]

        for categoria_info in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nome=categoria_info['nome'],
                defaults={'descricao': categoria_info['descricao']}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Categoria "{categoria.nome}" criada!')
                )

    def mostrar_status(self):
        """Mostra status das categorias NLAG e ERSA"""
        self.stdout.write('\n📊 STATUS DAS CATEGORIAS:')
        
        for nome in ['NLAG', 'ERSA']:
            try:
                categoria = Categoria.objects.get(nome=nome)
                produtos_count = categoria.produto_set.count()
                self.stdout.write(
                    f'  • {categoria.nome}: {produtos_count} produtos'
                )
                
                if produtos_count > 0:
                    self.stdout.write('    Produtos:')
                    for produto in categoria.produto_set.all()[:5]:  # Mostra até 5
                        self.stdout.write(f'      - {produto.codigo}: {produto.nome}')
                    if produtos_count > 5:
                        self.stdout.write(f'      ... e mais {produtos_count - 5} produtos')
                        
            except Categoria.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ {nome}: Não encontrada!')
                )

    def limpar_outras_categorias(self):
        """Remove categorias vazias que não sejam NLAG ou ERSA"""
        categorias_outras = Categoria.objects.exclude(
            nome__in=['NLAG', 'ERSA']
        ).filter(
            produto__isnull=True
        ).distinct()

        if categorias_outras.exists():
            self.stdout.write('\n🗑️ Categorias que serão removidas:')
            for categoria in categorias_outras:
                self.stdout.write(f'  • {categoria.nome}')
            
            if self.confirm_action('\nConfirma a remoção?'):
                count = categorias_outras.count()
                categorias_outras.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {count} categorias removidas!')
                )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Não há outras categorias vazias para remover.')
            )

    def mostrar_menu(self):
        """Mostra menu de opções"""
        self.mostrar_status()
        
        self.stdout.write('\n🔧 OPÇÕES DISPONÍVEIS:')
        self.stdout.write('  python manage.py gerenciar_categorias --status')
        self.stdout.write('  python manage.py gerenciar_categorias --limpar-outras')
        
        # Mostrar todas as categorias
        todas_categorias = Categoria.objects.all()
        if todas_categorias.count() > 2:
            self.stdout.write(f'\n📋 Todas as categorias ({todas_categorias.count()}):')
            for categoria in todas_categorias:
                produtos_count = categoria.produto_set.count()
                if categoria.nome in ['NLAG', 'ERSA']:
                    self.stdout.write(f'  ✅ {categoria.nome} ({produtos_count} produtos)')
                else:
                    self.stdout.write(f'  • {categoria.nome} ({produtos_count} produtos)')

    def confirm_action(self, message):
        """Confirma uma ação com o usuário"""
        response = input(f'{message} (s/N): ').lower().strip()
        return response in ['s', 'sim', 'yes', 'y']
