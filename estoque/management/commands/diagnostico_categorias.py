from django.core.management.base import BaseCommand
from estoque.models import Categoria, Produto
from estoque.forms import ProdutoForm


class Command(BaseCommand):
    help = 'Diagnóstica o sistema de categorias para mobile'

    def handle(self, *args, **options):
        self.stdout.write('🔍 DIAGNÓSTICO COMPLETO - CATEGORIAS MOBILE')
        self.stdout.write('=' * 60)

        # 1. Verificar categorias no banco
        self.stdout.write('\n📊 1. CATEGORIAS NO BANCO DE DADOS:')
        categorias = Categoria.objects.all()
        if categorias:
            for cat in categorias:
                produtos_count = cat.produto_set.count()
                self.stdout.write(f'  ✅ ID: {cat.id} | Nome: {cat.nome} | Produtos: {produtos_count}')
        else:
            self.stdout.write('  ❌ Nenhuma categoria encontrada!')

        # 2. Verificar formulário
        self.stdout.write('\n📝 2. CATEGORIAS NO FORMULÁRIO:')
        try:
            form = ProdutoForm()
            categoria_choices = form.fields['categoria'].queryset
            if categoria_choices:
                for cat in categoria_choices:
                    self.stdout.write(f'  ✅ {cat.id}: {cat.nome}')
            else:
                self.stdout.write('  ❌ Nenhuma categoria disponível no formulário!')
        except Exception as e:
            self.stdout.write(f'  ❌ Erro ao carregar formulário: {e}')

        # 3. Verificar produtos por categoria
        self.stdout.write('\n📦 3. PRODUTOS POR CATEGORIA:')
        for cat in categorias:
            produtos = cat.produto_set.filter(ativo=True)
            self.stdout.write(f'  📂 {cat.nome}:')
            if produtos:
                for produto in produtos:
                    self.stdout.write(f'    - {produto.codigo}: {produto.nome}')
            else:
                self.stdout.write('    (nenhum produto)')

        # 4. Verificar se há problemas de migração
        self.stdout.write('\n🔄 4. VERIFICAÇÃO DE INTEGRIDADE:')
        try:
            # Tentar criar um produto de teste (sem salvar)
            form_data = {
                'codigo': 'TEST001',
                'nome': 'Produto Teste',
                'categoria': categorias.first().id if categorias.exists() else None,
                'quantidade_atual': 10,
                'quantidade_minima': 5,
                'preco_custo': 10.00,
                'preco_venda': 15.00,
                'unidade_medida': 'UN',
                'ativo': True
            }
            form = ProdutoForm(data=form_data)
            if form.is_valid():
                self.stdout.write('  ✅ Formulário de produto válido')
            else:
                self.stdout.write('  ❌ Formulário inválido:')
                for field, errors in form.errors.items():
                    self.stdout.write(f'    - {field}: {errors}')
        except Exception as e:
            self.stdout.write(f'  ❌ Erro na validação: {e}')

        # 5. Comandos recomendados
        self.stdout.write('\n🔧 5. COMANDOS PARA CORRIGIR:')
        self.stdout.write('  python manage.py gerenciar_categorias --status')
        self.stdout.write('  python manage.py setup_categorias')
        
        # 6. Resumo final
        total_categorias = categorias.count()
        total_produtos = Produto.objects.filter(ativo=True).count()
        
        self.stdout.write('\n📋 6. RESUMO:')
        self.stdout.write(f'  • Total de categorias: {total_categorias}')
        self.stdout.write(f'  • Total de produtos ativos: {total_produtos}')
        
        if total_categorias >= 2 and 'NLAG' in [c.nome for c in categorias] and 'ERSA' in [c.nome for c in categorias]:
            self.stdout.write('  ✅ Categorias NLAG e ERSA configuradas corretamente!')
        else:
            self.stdout.write('  ❌ Problema nas categorias NLAG e ERSA!')

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🎯 DIAGNÓSTICO CONCLUÍDO!')
