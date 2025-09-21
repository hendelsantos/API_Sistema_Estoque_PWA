from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Categorias"
        ordering = ['nome']


class Fornecedor(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']


class Produto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, help_text="Código do produto/SKU")
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, blank=True, null=True)
    
    # Controle de estoque
    quantidade_atual = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        validators=[MinValueValidator(0)]
    )
    quantidade_minima = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Quantidade mínima para alerta de estoque baixo"
    )
    
    # Preços
    preco_custo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    preco_venda = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Informações adicionais
    unidade_medida = models.CharField(
        max_length=10, 
        default='UN',
        help_text="Ex: UN, KG, LT, M"
    )
    localizacao = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Localização física no estoque"
    )
    
    # QR Code para identificação
    qr_code = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Código QR para busca rápida"
    )
    
    # Imagem do produto
    imagem = models.ImageField(
        upload_to='produtos/', 
        blank=True, 
        null=True
    )
    
    # Status
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    def save(self, *args, **kwargs):
        # Gerar QR code se não existir
        if not self.qr_code:
            self.qr_code = f"PROD-{self.codigo}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def estoque_baixo(self):
        """Verifica se o produto está com estoque baixo"""
        return self.quantidade_atual <= self.quantidade_minima

    @property
    def valor_total_estoque(self):
        """Calcula o valor total do estoque atual"""
        return self.quantidade_atual * self.preco_custo

    class Meta:
        ordering = ['nome']


class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('AJUSTE', 'Ajuste'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='movimentacoes')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    quantidade_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_atual = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Informações da movimentação
    motivo = models.CharField(max_length=200, help_text="Motivo da movimentação")
    observacao = models.TextField(blank=True, null=True)
    documento = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Número do documento (NF, pedido, etc.)"
    )
    
    # Auditoria
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_movimentacao = models.DateTimeField(default=timezone.now)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.tipo} - {self.quantidade}"

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']


class InventarioFisico(models.Model):
    """Controle de inventários físicos realizados"""
    
    STATUS_CHOICES = [
        ('PLANEJADO', 'Planejado'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PLANEJADO')
    
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField(blank=True, null=True)
    
    # Auditoria
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='inventarios_criados')
    realizado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='inventarios_realizados',
        blank=True,
        null=True
    )
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} - {self.status}"

    class Meta:
        verbose_name = "Inventário Físico"
        verbose_name_plural = "Inventários Físicos"
        ordering = ['-data_inicio']


class ItemInventario(models.Model):
    """Itens contados em cada inventário"""
    
    inventario = models.ForeignKey(InventarioFisico, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    
    quantidade_sistema = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_contada = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True
    )
    
    diferenca = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacao = models.TextField(blank=True, null=True)
    
    contado_em = models.DateTimeField(blank=True, null=True)
    contado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if self.quantidade_contada is not None:
            self.diferenca = self.quantidade_contada - self.quantidade_sistema
            if not self.contado_em:
                self.contado_em = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.inventario.nome} - {self.produto.nome}"

    class Meta:
        verbose_name = "Item de Inventário"
        verbose_name_plural = "Itens de Inventário"
        unique_together = ['inventario', 'produto']
