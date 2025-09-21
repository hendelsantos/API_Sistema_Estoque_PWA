from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, Count, F
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Produto, Categoria, Fornecedor, MovimentacaoEstoque
from .forms import ProdutoForm, MovimentacaoForm, CategoriaForm, FornecedorForm



def dashboard(request):
    """Dashboard principal com estatísticas gerais"""
    
    # Estatísticas gerais
    total_produtos = Produto.objects.filter(ativo=True).count()
    produtos_baixo_estoque = Produto.objects.filter(
        ativo=True,
        quantidade_atual__lte=F('quantidade_minima')
    ).count()
    
    valor_total_estoque = Produto.objects.filter(ativo=True).aggregate(
        total=Sum(F('quantidade_atual') * F('preco_custo'))
    )['total'] or 0
    
    # Produtos com estoque baixo
    produtos_alerta = Produto.objects.filter(
        ativo=True,
        quantidade_atual__lte=F('quantidade_minima')
    )[:5]
    
    # Últimas movimentações
    ultimas_movimentacoes = MovimentacaoEstoque.objects.select_related(
        'produto', 'usuario'
    ).order_by('-data_movimentacao')[:10]
    
    context = {
        'total_produtos': total_produtos,
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'valor_total_estoque': valor_total_estoque,
        'produtos_alerta': produtos_alerta,
        'ultimas_movimentacoes': ultimas_movimentacoes,
    }
    
    return render(request, 'estoque/dashboard.html', context)



def produto_list(request):
    """Lista de produtos com busca e filtros"""
    
    produtos = Produto.objects.filter(ativo=True).select_related('categoria', 'fornecedor')
    
    # Busca
    search = request.GET.get('search', '')
    if search:
        produtos = produtos.filter(
            Q(nome__icontains=search) |
            Q(codigo__icontains=search) |
            Q(qr_code__icontains=search)
        )
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)
    
    fornecedor_id = request.GET.get('fornecedor')
    if fornecedor_id:
        produtos = produtos.filter(fornecedor_id=fornecedor_id)
    
    estoque_baixo = request.GET.get('estoque_baixo')
    if estoque_baixo == '1':
        produtos = produtos.filter(quantidade_atual__lte=F('quantidade_minima'))
    
    # Ordenação
    ordem = request.GET.get('ordem', 'nome')
    if ordem in ['nome', '-nome', 'quantidade_atual', '-quantidade_atual', 'codigo', '-codigo']:
        produtos = produtos.order_by(ordem)
    
    # Paginação
    paginator = Paginator(produtos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Para filtros
    categorias = Categoria.objects.all()
    fornecedores = Fornecedor.objects.filter(ativo=True)
    
    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'fornecedores': fornecedores,
        'search': search,
        'categoria_id': categoria_id,
        'fornecedor_id': fornecedor_id,
        'estoque_baixo': estoque_baixo,
        'ordem': ordem,
    }
    
    return render(request, 'estoque/produto_list.html', context)



def produto_detail(request, pk):
    """Detalhes do produto"""
    produto = get_object_or_404(Produto, pk=pk, ativo=True)
    
    # Histórico de movimentações
    movimentacoes = produto.movimentacoes.select_related('usuario').order_by('-data_movimentacao')[:20]
    
    context = {
        'produto': produto,
        'movimentacoes': movimentacoes,
    }
    
    return render(request, 'estoque/produto_detail.html', context)



def produto_create(request):
    """Criar novo produto"""
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto "{produto.nome}" criado com sucesso!')
            return redirect('estoque:produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm()
    
    context = {'form': form, 'titulo': 'Novo Produto'}
    return render(request, 'estoque/produto_form.html', context)



def produto_update(request, pk):
    """Atualizar produto"""
    produto = get_object_or_404(Produto, pk=pk, ativo=True)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto "{produto.nome}" atualizado com sucesso!')
            return redirect('estoque:produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)
    
    context = {'form': form, 'produto': produto, 'titulo': 'Editar Produto'}
    return render(request, 'estoque/produto_form.html', context)



def produto_delete(request, pk):
    """Desativar produto (soft delete)"""
    produto = get_object_or_404(Produto, pk=pk, ativo=True)
    
    if request.method == 'POST':
        produto.ativo = False
        produto.save()
        messages.success(request, f'Produto "{produto.nome}" removido com sucesso!')
        return redirect('estoque:produto_list')
    
    context = {'produto': produto}
    return render(request, 'estoque/produto_confirm_delete.html', context)



def buscar_qr(request):
    """Página do scanner QR"""
    produto = None
    
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code', '').strip()
        if qr_code:
            try:
                produto = Produto.objects.get(qr_code=qr_code, ativo=True)
            except Produto.DoesNotExist:
                messages.error(request, 'Produto não encontrado com este código QR.')
    
    context = {'produto': produto}
    return render(request, 'estoque/buscar_qr.html', context)



def movimentacao_list(request):
    """Lista de movimentações"""
    movimentacoes = MovimentacaoEstoque.objects.select_related(
        'produto', 'usuario'
    ).order_by('-data_movimentacao')
    
    # Filtros
    produto_id = request.GET.get('produto')
    if produto_id:
        movimentacoes = movimentacoes.filter(produto_id=produto_id)
    
    tipo = request.GET.get('tipo')
    if tipo and tipo in ['ENTRADA', 'SAIDA', 'AJUSTE']:
        movimentacoes = movimentacoes.filter(tipo=tipo)
    
    # Paginação
    paginator = Paginator(movimentacoes, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tipo': tipo,
        'produto_id': produto_id,
    }
    
    return render(request, 'estoque/movimentacao_list.html', context)



def entrada_estoque(request, produto_id):
    """Entrada de estoque"""
    produto = get_object_or_404(Produto, pk=produto_id, ativo=True)
    
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.produto = produto
            movimentacao.tipo = 'ENTRADA'
            movimentacao.usuario = request.user
            movimentacao.quantidade_anterior = produto.quantidade_atual
            
            # Atualizar quantidade do produto
            produto.quantidade_atual += movimentacao.quantidade
            movimentacao.quantidade_atual = produto.quantidade_atual
            
            movimentacao.save()
            produto.save()
            
            messages.success(request, f'Entrada registrada! Novo estoque: {produto.quantidade_atual}')
            return redirect('estoque:produto_detail', pk=produto.pk)
    else:
        form = MovimentacaoForm()
    
    context = {
        'form': form, 
        'produto': produto, 
        'titulo': 'Entrada de Estoque',
        'tipo': 'ENTRADA'
    }
    return render(request, 'estoque/movimentacao_form.html', context)



def saida_estoque(request, produto_id):
    """Saída de estoque"""
    produto = get_object_or_404(Produto, pk=produto_id, ativo=True)
    
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            
            # Verificar se há estoque suficiente
            if movimentacao.quantidade > produto.quantidade_atual:
                messages.error(request, 'Quantidade insuficiente em estoque!')
                return render(request, 'estoque/movimentacao_form.html', {
                    'form': form, 'produto': produto, 'titulo': 'Saída de Estoque', 'tipo': 'SAIDA'
                })
            
            movimentacao.produto = produto
            movimentacao.tipo = 'SAIDA'
            movimentacao.usuario = request.user
            movimentacao.quantidade_anterior = produto.quantidade_atual
            
            # Atualizar quantidade do produto
            produto.quantidade_atual -= movimentacao.quantidade
            movimentacao.quantidade_atual = produto.quantidade_atual
            
            movimentacao.save()
            produto.save()
            
            messages.success(request, f'Saída registrada! Novo estoque: {produto.quantidade_atual}')
            return redirect('estoque:produto_detail', pk=produto.pk)
    else:
        form = MovimentacaoForm()
    
    context = {
        'form': form, 
        'produto': produto, 
        'titulo': 'Saída de Estoque',
        'tipo': 'SAIDA'
    }
    return render(request, 'estoque/movimentacao_form.html', context)



def ajuste_estoque(request, produto_id):
    """Ajuste de estoque"""
    produto = get_object_or_404(Produto, pk=produto_id, ativo=True)
    
    if request.method == 'POST':
        nova_quantidade = request.POST.get('nova_quantidade')
        motivo = request.POST.get('motivo')
        
        try:
            nova_quantidade = float(nova_quantidade)
            
            if nova_quantidade < 0:
                messages.error(request, 'A quantidade não pode ser negativa!')
                return redirect('estoque:produto_detail', pk=produto.pk)
            
            # Criar movimentação de ajuste
            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo='AJUSTE',
                quantidade=abs(nova_quantidade - produto.quantidade_atual),
                quantidade_anterior=produto.quantidade_atual,
                quantidade_atual=nova_quantidade,
                motivo=motivo or 'Ajuste de estoque',
                usuario=request.user
            )
            
            produto.quantidade_atual = nova_quantidade
            produto.save()
            
            messages.success(request, f'Estoque ajustado! Nova quantidade: {nova_quantidade}')
            
        except (ValueError, TypeError):
            messages.error(request, 'Quantidade inválida!')
    
    return redirect('estoque:produto_detail', pk=produto.pk)



def categoria_list(request):
    """Lista de categorias"""
    categorias = Categoria.objects.all()
    return render(request, 'estoque/categoria_list.html', {'categorias': categorias})



def fornecedor_list(request):
    """Lista de fornecedores"""
    fornecedores = Fornecedor.objects.filter(ativo=True)
    return render(request, 'estoque/fornecedor_list.html', {'fornecedores': fornecedores})



def relatorios(request):
    """Página de relatórios"""
    return render(request, 'estoque/relatorios.html')



def estoque_baixo(request):
    """Produtos com estoque baixo"""
    produtos = Produto.objects.filter(
        ativo=True,
        quantidade_atual__lte=F('quantidade_minima')
    ).select_related('categoria')
    
    context = {'produtos': produtos}
    return render(request, 'estoque/estoque_baixo.html', context)


# HTMX Views

def produto_card_htmx(request, pk):
    """Card do produto para HTMX"""
    produto = get_object_or_404(Produto, pk=pk, ativo=True)
    return render(request, 'estoque/partials/produto_card.html', {'produto': produto})



def buscar_produtos_htmx(request):
    """Busca de produtos via HTMX"""
    search = request.GET.get('search', '')
    produtos = []
    
    if len(search) >= 2:
        produtos = Produto.objects.filter(
            Q(nome__icontains=search) |
            Q(codigo__icontains=search) |
            Q(qr_code__icontains=search),
            ativo=True
        )[:10]
    
    return render(request, 'estoque/partials/produto_search_results.html', {
        'produtos': produtos, 'search': search
    })
