from django.core.management.base import BaseCommand
from django.db import transaction
from estoque.models import Categoria, Produto


class Command(BaseCommand):
    help = 'Força a reconfiguração das categorias NLAG e ERSA'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a reconfiguração sem perguntar',
        )

    def handle(self, *args, **options):
        self.stdout.write('🔧 FORÇANDO RECONFIGURAÇÃO - CATEGORIAS NLAG E ERSA')
        self.stdout.write('=' * 60)

        with transaction.atomic():
            # 1. Verificar estado atual
            self.stdout.write('\n📊 Estado atual:')
            for cat in Categoria.objects.all():
                produtos_count = cat.produto_set.count()
                self.stdout.write(f'  • {cat.nome}: {produtos_count} produtos')

            # 2. Garantir que NLAG e ERSA existem
            nlag, created_nlag = Categoria.objects.get_or_create(
                nome='NLAG',
                defaults={'descricao': 'Categoria NLAG - Produtos específicos'}
            )
            if created_nlag:
                self.stdout.write('✅ Categoria NLAG criada')
            else:
                self.stdout.write('ℹ️ Categoria NLAG já existe')

            ersa, created_ersa = Categoria.objects.get_or_create(
                nome='ERSA',
                defaults={'descricao': 'Categoria ERSA - Produtos específicos'}
            )
            if created_ersa:
                self.stdout.write('✅ Categoria ERSA criada')
            else:
                self.stdout.write('ℹ️ Categoria ERSA já existe')

            # 3. Migrar produtos sem categoria para NLAG
            produtos_sem_categoria = Produto.objects.filter(categoria__isnull=True)
            if produtos_sem_categoria.exists():
                count = produtos_sem_categoria.update(categoria=nlag)
                self.stdout.write(f'✅ {count} produtos migrados para NLAG')

            # 4. Verificar produtos órfãos (categoria inexistente)
            produtos_orfaos = Produto.objects.exclude(
                categoria__in=Categoria.objects.all()
            )
            if produtos_orfaos.exists():
                count = produtos_orfaos.update(categoria=nlag)
                self.stdout.write(f'✅ {count} produtos órfãos migrados para NLAG')

            # 5. Remover categorias vazias (exceto NLAG e ERSA)
            if options['force'] or self.confirm_action('Remover categorias vazias (exceto NLAG e ERSA)?'):
                categorias_vazias = Categoria.objects.exclude(
                    nome__in=['NLAG', 'ERSA']
                ).filter(
                    produto__isnull=True
                ).distinct()

                if categorias_vazias.exists():
                    nomes_removidas = list(categorias_vazias.values_list('nome', flat=True))
                    categorias_vazias.delete()
                    self.stdout.write(f'✅ Categorias removidas: {", ".join(nomes_removidas)}')
                else:
                    self.stdout.write('ℹ️ Nenhuma categoria vazia para remover')

        # 6. Resultado final
        self.stdout.write('\n📋 RESULTADO FINAL:')
        for cat in Categoria.objects.all():
            produtos_count = cat.produto_set.count()
            self.stdout.write(f'  ✅ {cat.nome}: {produtos_count} produtos')

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🎯 RECONFIGURAÇÃO CONCLUÍDA!')
        self.stdout.write('📱 As categorias agora devem aparecer corretamente no mobile!')

    def confirm_action(self, message):
        """Confirma uma ação com o usuário"""
        response = input(f'{message} (s/N): ').lower().strip()
        return response in ['s', 'sim', 'yes', 'y']
