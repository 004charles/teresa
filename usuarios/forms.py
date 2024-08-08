from django import forms
from .models import Produtos, Cliente, Empresas, Marca_produto, Categoria_produto, Fornecedor, Pedido, Pedido_empresa, Contato_empresa

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg', 'placeholder': field.label})

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['foto', 'nome', 'email', 'senha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg', 'placeholder': field.label})

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg', 'placeholder': field.label})

class MarcaProdutoForm(forms.ModelForm):
    class Meta:
        model = Marca_produto
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg', 'placeholder': field.label})

class CategoriaProdutoForm(forms.ModelForm):
    class Meta:
        model = Categoria_produto
        fields = ['nome']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg', 'placeholder': field.label})

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'local']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg', 'placeholder': field.label})

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['endereco']
        widgets = {
            'endereco': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'cols': 80,
                'rows': 4,
                'placeholder': 'Digite seu endereço'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('usuario', None)

class PedidoEmpresaForm(forms.ModelForm):
    class Meta:
        model = Pedido_empresa
        fields = ['endereco']
        widgets = {
            'endereco': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'cols': 80,
                'rows': 4,
                'placeholder': 'Digite o endereço da empresa'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['endereco'].label = 'Endereço da Empresa'

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato_empresa
        fields = ['nome', 'email', 'assunto', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Digite seu nome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Digite seu email'
            }),
            'assunto': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Digite o assunto'
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': 4,
                'placeholder': 'Digite sua mensagem'
            }),
        }


   

from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'mensagem': forms.Textarea(attrs={'rows': 4}),
        }

