from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Produtos
    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/criar/', views.produto_create, name='produto_create'),
    path('produtos/<int:pk>/', views.produto_detail, name='produto_detail'),
    path('produtos/<int:pk>/editar/', views.produto_update, name='produto_update'),
    path('produtos/<int:pk>/deletar/', views.produto_delete, name='produto_delete'),
    
    # Busca por QR Code
    path('buscar-qr/', views.buscar_qr, name='buscar_qr'),
    
    # Movimentações
    path('movimentacoes/', views.movimentacao_list, name='movimentacao_list'),
    path('movimentacoes/entrada/<int:produto_id>/', views.entrada_estoque, name='entrada_estoque'),
    path('movimentacoes/saida/<int:produto_id>/', views.saida_estoque, name='saida_estoque'),
    path('movimentacoes/ajuste/<int:produto_id>/', views.ajuste_estoque, name='ajuste_estoque'),
    
    # Categorias e Fornecedores
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('fornecedores/', views.fornecedor_list, name='fornecedor_list'),
    
    # Relatórios
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/estoque-baixo/', views.estoque_baixo, name='estoque_baixo'),
    
    # HTMX endpoints
    path('htmx/produto-card/<int:pk>/', views.produto_card_htmx, name='produto_card_htmx'),
    path('htmx/buscar-produtos/', views.buscar_produtos_htmx, name='buscar_produtos_htmx'),
]
