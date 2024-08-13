from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from decimal import Decimal


from django.db import models

class Gerente(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=40)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Conta do gerente"


from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


    class Meta:
        verbose_name_plural = "Conta dos Clientes"


class Empresas(models.Model):
    nome = models.CharField(max_length=100)
    nif = models.CharField(max_length=60)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Conta dos Empresas"


class Marca_produto(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Marcas dos produtos"


class Categoria_produto(models.Model):
    nome = models.CharField(max_length=40)
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Categoria do produto"


class Condicao(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Condição do produto"


class Fornecedor(models.Model):
    nome = models.CharField(max_length=50)
    local = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Fornecedores"


class Produtos(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=600)
    marca = models.ForeignKey(Marca_produto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria_produto, on_delete=models.CASCADE)
    estoque = models.CharField(max_length=40)
    preco = models.FloatField()
    preco_promocional = models.FloatField()
    imagem = models.FileField(upload_to='imagem/')
    peso = models.FloatField()
    dimensao = models.CharField(max_length=50)
    compatibilidade = models.CharField(max_length=50)
    quantidade_fornecida = models.IntegerField()
    material = models.CharField(max_length=50)
    condicao = models.ForeignKey(Condicao, on_delete=models.CASCADE)
    instrucao_instalacao = models.TextField(max_length=300, blank=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    garantia = models.CharField(max_length=50)
    prazo_entrega = models.CharField(max_length=50)
    data_criacao = models.DateTimeField(default=timezone.now)  # Novo campo adicionado

    def __str__(self):
        return self.nome
    
class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey('Carrinho', on_delete=models.CASCADE, related_name='itens_carrinho', null=True, blank=True)
    carrinho_empresa = models.ForeignKey('Carrinho_empresa', on_delete=models.CASCADE, related_name='itens_carrinho_empresa', null=True, blank=True)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantidade * self.produto.preco

    def __str__(self):
        return f'{self.produto.nome} ({self.quantidade})'


class Carrinho(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='carrinho')
    produtos = models.ManyToManyField(Produtos, through=ItemCarrinho, related_name='carrinhos_cliente')
    endereco = models.CharField(max_length=255, blank=True, null=True)  # Campo para armazenar o endereço

class Carrinho_empresa(models.Model):
    empresa = models.OneToOneField(Empresas, on_delete=models.CASCADE, related_name='carrinhos_empresa')
    produtos = models.ManyToManyField(Produtos, through=ItemCarrinho, related_name='carrinhos_empresa')
    def __str__(self):
        return f'Carrinho da Empresa: {self.empresa.nome}'

class Pedido(models.Model):
    imagem = models.FileField(upload_to='imagem/')
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    endereco = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'Pedido {self.id} para {self.usuario.nome} em {self.data.strftime("%d/%m/%Y")}'
    def total(self):
        # Usar o related_name definido
        return sum(item.quantidade * item.produto.preco for item in self.item_pedido_set.all())
    
    
class Pedido_empresa(models.Model):
    imagem = models.FileField(upload_to='imagem/')
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    endereco = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'Pedido {self.id} para {self.empresa.nome} em {self.data.strftime("%d/%m/%Y")}'

    def subtotal(self):
        return sum(item.quantidade * item.preco for item in self.itens.all())

    def imposto(self):
        return Decimal(self.subtotal()) * Decimal('0.10')

    def total(self):
        return self.subtotal() + self.imposto()

    def total(self):
        return sum(item.quantidade * item.produto.preco for item in self.itens.all())


class ItemPedidoEmpresa(models.Model):
    pedido = models.ForeignKey(Pedido_empresa, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome} no pedido {self.pedido.id}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='item_pedido_set')
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    
    def subtotal(self):
        return self.quantidade * self.produto.preco

class Chat(models.Model):
     mensagem = models.ForeignKey(Gerente, on_delete=models.CASCADE)

     def __str__(self):
          return self.nome
     
     class Meta:
          verbose_name_plural = "chat online"

class contactar(models.Model):
     email = models.EmailField(max_length=50)
     assunto = models.TextField(max_length=200)

     def __str__(self):
          return self.nome
     
     class Meta:
          verbose_name_plural = "Contactos/Dividas"


from django.utils import timezone

def generate_fatura_number():
    return 'F-' + timezone.now().strftime("%Y%m%d%H%M%S")

class Fatura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)  
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, null=True, blank=True)  
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE) 
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao = models.DateTimeField(default=timezone.now) 

    
    
class Estoque(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE, related_name='estoques')
    quantidade = models.PositiveIntegerField()
    data_ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade} em estoque'




class Noticia(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='imagem/')
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Notícias"


class Marca_index(models.Model):
    nome = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='imagem/')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Marcas na pagina principal"


class Video(models.Model):
    video = models.URLField()

    def __str__(self):
        return self.video
    
    class Meta:
        verbose_name_plural = "Video Principal"


class Contato_empresa(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    assunto = models.CharField(max_length=255)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Iban(models.Model):
    ibam = models.CharField(max_length = 100)

    def __str__(self):
        return self.ibam
    
class Ticket(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.nome}"
    
'''
class Endereco(models.Model):
    cliente = models.OneToOneField('Cliente', on_delete=models.CASCADE, related_name='endereco')
    cidade = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    cep = models.CharField(max_length=10)
    data_adicao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}, {self.pais}'

    class Meta:
        verbose_name_plural = "Endereços"
'''