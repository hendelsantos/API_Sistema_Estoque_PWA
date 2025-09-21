from django import forms
from django.core.exceptions import ValidationError
from .models import Produto, MovimentacaoEstoque, Categoria, Fornecedor


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'codigo', 'nome', 'descricao', 'categoria', 'fornecedor',
            'quantidade_atual', 'quantidade_minima', 'preco_custo', 
            'preco_venda', 'unidade_medida', 'localizacao', 'imagem', 'ativo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único do produto'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição detalhada'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_atual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'quantidade_minima': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'unidade_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: UN, KG, LT'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Estante A, Prateleira 2'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'codigo': 'Código',
            'nome': 'Nome do Produto',
            'descricao': 'Descrição',
            'categoria': 'Categoria',
            'fornecedor': 'Fornecedor',
            'quantidade_atual': 'Quantidade Atual',
            'quantidade_minima': 'Quantidade Mínima',
            'preco_custo': 'Preço de Custo (R$)',
            'preco_venda': 'Preço de Venda (R$)',
            'unidade_medida': 'Unidade de Medida',
            'localizacao': 'Localização no Estoque',
            'imagem': 'Imagem do Produto',
            'ativo': 'Produto Ativo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas fornecedores ativos
        self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True)
        self.fields['fornecedor'].empty_label = "Selecione um fornecedor"
        
        # Campo categoria obrigatório
        self.fields['categoria'].empty_label = "Selecione uma categoria"

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        
        # Verificar se o código já existe (excluindo o próprio objeto se for edição)
        qs = Produto.objects.filter(codigo=codigo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError("Já existe um produto com este código.")
        
        return codigo

    def clean(self):
        cleaned_data = super().clean()
        preco_custo = cleaned_data.get('preco_custo')
        preco_venda = cleaned_data.get('preco_venda')
        quantidade_atual = cleaned_data.get('quantidade_atual')
        quantidade_minima = cleaned_data.get('quantidade_minima')

        # Validar se preço de venda é maior que preço de custo
        if preco_custo and preco_venda and preco_venda < preco_custo:
            self.add_error('preco_venda', 'O preço de venda deve ser maior ou igual ao preço de custo.')

        # Validar quantidades
        if quantidade_atual and quantidade_atual < 0:
            self.add_error('quantidade_atual', 'A quantidade atual não pode ser negativa.')
        
        if quantidade_minima and quantidade_minima < 0:
            self.add_error('quantidade_minima', 'A quantidade mínima não pode ser negativa.')

        return cleaned_data


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ['quantidade', 'motivo', 'observacao', 'documento']
        widgets = {
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01', 
                'min': '0.01',
                'placeholder': 'Quantidade a movimentar'
            }),
            'motivo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: Compra, Venda, Inventário...',
                'maxlength': '200'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)'
            }),
            'documento': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nº da NF, Pedido, etc. (opcional)'
            }),
        }
        labels = {
            'quantidade': 'Quantidade',
            'motivo': 'Motivo da Movimentação',
            'observacao': 'Observações',
            'documento': 'Número do Documento',
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        if quantidade <= 0:
            raise ValidationError("A quantidade deve ser maior que zero.")
        return quantidade


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome da categoria'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Descrição da categoria (opcional)'
            }),
        }
        labels = {
            'nome': 'Nome da Categoria',
            'descricao': 'Descrição',
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome']
        
        # Verificar se já existe categoria com este nome
        qs = Categoria.objects.filter(nome__iexact=nome)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError("Já existe uma categoria com este nome.")
        
        return nome


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'telefone', 'email', 'endereco', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome do fornecedor'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '00.000.000/0000-00'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '(11) 99999-9999'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'email@fornecedor.com'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Endereço completo'
            }),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nome': 'Nome/Razão Social',
            'cnpj': 'CNPJ',
            'telefone': 'Telefone',
            'email': 'E-mail',
            'endereco': 'Endereço',
            'ativo': 'Fornecedor Ativo',
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj', '')
        if cnpj:
            # Remover caracteres especiais
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
            
            # Validar tamanho
            if len(cnpj_limpo) != 14:
                raise ValidationError("CNPJ deve ter 14 dígitos.")
            
            # Verificar se já existe outro fornecedor com este CNPJ
            qs = Fornecedor.objects.filter(cnpj=cnpj)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise ValidationError("Já existe um fornecedor com este CNPJ.")
        
        return cnpj

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            # Verificar se já existe outro fornecedor com este email
            qs = Fornecedor.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise ValidationError("Já existe um fornecedor com este e-mail.")
        
        return email


class BuscaQRForm(forms.Form):
    qr_code = forms.CharField(
        label='Código QR',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite ou escaneie o código QR',
            'autofocus': True
        })
    )


class FiltroMovimentacaoForm(forms.Form):
    TIPO_CHOICES = [
        ('', 'Todos os tipos'),
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('AJUSTE', 'Ajuste'),
    ]
    
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.filter(ativo=True),
        required=False,
        empty_label="Todos os produtos",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
