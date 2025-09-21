from django.core.management.base import BaseCommand
from estoque.models import Categoria


class Command(BaseCommand):
    help = 'Configura categorias básicas: NLAG e ERSA'

    def handle(self, *args, **options):
        self.stdout.write('🏷️ Configurando categorias: NLAG e ERSA')
        self.stdout.write('=' * 50)

        # Verificar categorias existentes
        categorias_existentes = list(Categoria.objects.values_list('nome', flat=True))
        if categorias_existentes:
            self.stdout.write(f'📋 Categorias existentes: {", ".join(categorias_existentes)}')
        
        # Criar as duas categorias principais
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
                    self.style.SUCCESS(f'✅ Categoria "{categoria.nome}" criada com sucesso!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Categoria "{categoria.nome}" já existe.')
                )

        # Mostrar resumo
        total_categorias = Categoria.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'\n📊 Total de categorias no sistema: {total_categorias}')
        )
        
        # Listar todas as categorias
        self.stdout.write('\n📋 Categorias disponíveis:')
        for categoria in Categoria.objects.all():
            produtos_count = categoria.produto_set.count()
            self.stdout.write(f'  • {categoria.nome} - {categoria.descricao} ({produtos_count} produtos)')

        # Perguntar se quer remover outras categorias (se houver mais de 2)
        if total_categorias > 2:
            self.stdout.write('\n⚠️ Existem outras categorias além de NLAG e ERSA.')
            if self.confirm_action('Deseja ver quais categorias podem ser removidas?'):
                self.mostrar_categorias_removiveis()

    def confirm_action(self, message):
        """Confirma uma ação com o usuário"""
        response = input(f'{message} (s/N): ').lower().strip()
        return response in ['s', 'sim', 'yes', 'y']
    
    def mostrar_categorias_removiveis(self):
        """Mostra categorias que podem ser removidas (sem produtos)"""
        # Categorias que queremos manter
        categorias_principais = ['NLAG', 'ERSA']
        
        categorias_vagas = Categoria.objects.filter(
            produto__isnull=True
        ).exclude(
            nome__in=categorias_principais
        ).distinct()
        
        categorias_com_produtos = Categoria.objects.exclude(produto__isnull=True).distinct()
        
        if categorias_vagas.exists():
            self.stdout.write('\n🗑️ Categorias vazias (podem ser removidas):')
            for categoria in categorias_vagas:
                self.stdout.write(f'  • {categoria.nome}')
        
        if categorias_com_produtos.exists():
            self.stdout.write('\n🔒 Categorias com produtos (não podem ser removidas):')
            for categoria in categorias_com_produtos:
                produtos_count = categoria.produto_set.count()
                self.stdout.write(f'  • {categoria.nome} ({produtos_count} produtos)')
        
        # Mostrar categorias principais
        categorias_nlag_ersa = Categoria.objects.filter(nome__in=categorias_principais)
        if categorias_nlag_ersa.exists():
            self.stdout.write('\n✅ Categorias principais (NLAG e ERSA):')
            for categoria in categorias_nlag_ersa:
                produtos_count = categoria.produto_set.count()
                self.stdout.write(f'  • {categoria.nome} ({produtos_count} produtos)')
        
        # Oferecer remoção das vazias (exceto NLAG e ERSA)
        if categorias_vagas.exists():
            if self.confirm_action('\nDeseja remover apenas as categorias vazias (mantendo NLAG e ERSA)?'):
                categorias_vagas.delete()
                self.stdout.write(self.style.SUCCESS('✅ Categorias vazias removidas! NLAG e ERSA foram mantidas.'))
