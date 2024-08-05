from .models import Produtos
from django import forms
from .models import Cliente
from .models import Empresas
from .models import Marca_produto
from .models import Produtos, Contato_empresa
from .models import Categoria_produto, Pedido_empresa


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = '__all__'

from .models import Fornecedor

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = '__all__'  # Inclui todos os campos do modelo Produtos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes de Bootstrap aos widgets
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})



class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'}) 


from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['foto', 'nome', 'email', 'senha']

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = '__all__' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'}) 

class MarcaProdutoForm(forms.ModelForm):
    class Meta:
        model = Marca_produto
        fields = ['nome']



class CategoriaProdutoForm(forms.ModelForm):
    class Meta:
        model = Categoria_produto
        fields = ['nome']



class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'local']

from .models import Pedido

# forms.py
from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['endereco']
        widgets = {
            'endereco': forms.Textarea(attrs={
                'class': 'form-control',
                'cols': 80, 'rows': 4,
                'placeholder': 'Digite seu endereço'
            }),
        }

    def __init__(self, *args, **kwargs):
        # Remover o campo 'usuario' do formulário, pois ele não deve ser editável pelo usuário
        super().__init__(*args, **kwargs)
        self.fields.pop('usuario', None)


class PedidoEmpresaForm(forms.ModelForm):
    class Meta:
        model = Pedido_empresa
        fields = ['endereco']  # Ajuste conforme os campos necessários no seu modelo Pedido_empresa
        widgets = {
            'endereco': forms.Textarea(attrs={
                'class': 'form-control',
                'cols': 80,
                'rows': 4,
                'placeholder': 'Digite o endereço da empresa'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajuste os campos se necessário
        self.fields['endereco'].label = 'Endereço da Empresa'

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato_empresa
        fields = ['nome', 'email', 'assunto', 'mensagem']