from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Categoria, Fornecedor, Produto, MovimentacaoEstoque, 
    InventarioFisico, ItemInventario
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'criado_em']
    search_fields = ['nome']
    list_filter = ['criado_em']


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'telefone', 'email', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['nome', 'cnpj', 'email']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'nome', 'categoria', 'quantidade_atual', 
        'quantidade_minima', 'estoque_status', 'preco_venda', 'ativo'
    ]
    list_filter = ['categoria', 'fornecedor', 'ativo', 'criado_em']
    search_fields = ['codigo', 'nome', 'qr_code']
    readonly_fields = ['qr_code', 'criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'nome', 'descricao', 'categoria', 'fornecedor')
        }),
        ('Controle de Estoque', {
            'fields': ('quantidade_atual', 'quantidade_minima', 'unidade_medida', 'localizacao')
        }),
        ('Preços', {
            'fields': ('preco_custo', 'preco_venda')
        }),
        ('Identificação', {
            'fields': ('qr_code', 'imagem')
        }),
        ('Status e Auditoria', {
            'fields': ('ativo', 'criado_em', 'atualizado_em')
        }),
    )

    def estoque_status(self, obj):
        if obj.estoque_baixo:
            return format_html(
                '<span style="color: red; font-weight: bold;">⚠️ Baixo</span>'
            )
        return format_html('<span style="color: green;">✓ Normal</span>')
    
    estoque_status.short_description = 'Status Estoque'


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = [
        'produto', 'tipo', 'quantidade', 'quantidade_anterior', 
        'quantidade_atual', 'usuario', 'data_movimentacao'
    ]
    list_filter = ['tipo', 'data_movimentacao', 'usuario']
    search_fields = ['produto__nome', 'produto__codigo', 'motivo', 'documento']
    readonly_fields = ['criado_em']
    date_hierarchy = 'data_movimentacao'


class ItemInventarioInline(admin.TabularInline):
    model = ItemInventario
    extra = 0
    readonly_fields = ['diferenca']


@admin.register(InventarioFisico)
class InventarioFisicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'status', 'data_inicio', 'data_fim', 'criado_por']
    list_filter = ['status', 'data_inicio']
    search_fields = ['nome', 'descricao']
    inlines = [ItemInventarioInline]
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(ItemInventario)
class ItemInventarioAdmin(admin.ModelAdmin):
    list_display = [
        'inventario', 'produto', 'quantidade_sistema', 
        'quantidade_contada', 'diferenca', 'contado_por'
    ]
    list_filter = ['inventario', 'contado_em']
    search_fields = ['produto__nome', 'produto__codigo']
    readonly_fields = ['diferenca']
