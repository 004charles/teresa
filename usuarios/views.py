from django.shortcuts import render
from django.shortcuts import redirect
from .models import Gerente,Avaliacao , Cliente, Empresas, Marca_produto, Categoria_produto
from .models import Condicao, Fornecedor, Produtos, Carrinho_empresa, Iban
from .forms import MarcaProdutoForm
from .models import Categoria_produto, Carrinho,  Estoque, Noticia,  Marca_index, Video, ItemPedidoEmpresa
from .forms import CategoriaProdutoForm, ContatoForm, Contato_empresa
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import PyPDF2
from .forms import FornecedorForm, PedidoEmpresaForm
from django.core.files.storage import FileSystemStorage
from .models import Carrinho, ItemCarrinho, Pedido, ItemPedido, Pedido_empresa
from .forms import PedidoForm
from django.shortcuts import get_object_or_404, redirect

def index(request):
    produtos = Produtos.objects.all()
    marcas =  Marca_index.objects.all()
    noticias = Noticia.objects.all()
    video = Video.objects.create(video="https://www.youtube.com/embed/Get7rqXYrbQ")
    return render(request, 'index.html', {'produtos':produtos, 'marcas':marcas, 'noticias': noticias, 'video':video})

def gerente(request):
    # cadastrar produto
    # historico de venda
    # entrar em contacto
    # estoque
    # ver listar de clientes cadastrados
    # cadastrar cliente
    if 'gerente' in request.session:
        gerente_id = request.session['gerente']
        gerente = Gerente.objects.get(id=gerente_id)
        produto = Produtos.objects.all()
        estoques = Estoque.objects.all()
        contar_cliente = Cliente.objects.count()  
        contar_produto = Produtos.objects.count()
        contar_empresa = Empresas.objects.count()
        clientes = Cliente.objects.all()
        soma_total = contar_cliente + contar_empresa
        contar = Contato_empresa.objects.count()
        Pedido = Fatura.objects.count()
        categoria = Categoria_produto.objects.all()
        contactar = Contato_empresa.objects.all()
        return render(request, 'gerente.html', {'gerente':gerente, 'produto':produto, 'categoria':categoria, 'estoques':estoques, 'contactar':contactar, 'contar':contar, 'soma_total':soma_total, 'contar_produto':contar_produto, 'Pedido':Pedido, 'clientes': clientes})
    else:
        return HttpResponse("Você não está autenticado para acessar esta página.")

def nossos_clientes(request):
    contar = Contato_empresa.objects.count()
    contactar = Contato_empresa.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'nossos_clientes.html',{'clientes':clientes, 'contactar':contactar, 'contar':contar} )


def perfil_gerente(request):
    if 'gerente' in request.session:
        gerente_id = request.session['gerente']
        gerente = Gerente.objects.get(id=gerente_id)
        produto = Produtos.objects.all()
        categoria = Categoria_produto.objects.all()
        return render(request, 'perfil_gerente.html', {'gerente':gerente, 'produto':produto, 'categoria':categoria})
    else:
        return HttpResponse("Você não está autenticado para acessar esta página.")

def perfil_cliente(request):
    if 'cliente' in request.session:
        cliente_id = request.session['cliente']
        cliente = Cliente.objects.get(id=cliente_id)
        produto = Produtos.objects.all()
        categoria = Categoria_produto.objects.all()
        return render(request, 'perfil_cliente.html', {'cliente':cliente, 'produto':produto, 'categoria':categoria})
    else:
        return HttpResponse("Você não está autenticado para acessar esta página.")



def contactar_cliente(request):
    # contactar cliente
    pass

def listar_cliente(request):
    # llistar cliente
    pass

def historico_gerente(request):
    # historico de venda
    pass

def valida_login_gerente(request):
    status = request.POST.get('status')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    #senha = sha256(senha.encode()).hexdigest()
    
    gerente = Gerente.objects.filter(email = email, senha = senha) # tras 
    # do banco de dadosalguem onde o email senha igual a esse email, e senha que seja igual a essa senha...
    
    
    if len(gerente) == 0:
        return redirect('/vetor5/login_gerente/?status=1')
    
    if len(gerente) > 0:
        request.session['gerente'] = gerente[0].id
        return redirect('/vetor5/gerente/')

def login_gerente(request):
    return render(request, 'login_gerente.html')

def contactar_gerente(request):
    pass

def cliente(request):
    if 'cliente' in request.session:
        cliente_id = request.session['cliente']
        cliente = get_object_or_404(Cliente, id=cliente_id)
        produto = Produtos.objects.all()
        categoria = Categoria_produto.objects.all()
        pedidos = Pedido.objects.filter(usuario=cliente)
        # Passa os pedidos para o contexto
        return render(request, 'cliente.html', {'cliente': cliente, 'produto': produto, 'categoria': categoria, 'pedidos': pedidos})
    else:
        return HttpResponse("Você não está autenticado para acessar esta página.")


def remover_do_carrinho(request, produto_id):
    if 'cliente' in request.session:
        cliente_id = request.session['cliente']
        cliente = get_object_or_404(Cliente, id=cliente_id)
        # Busca o item do carrinho associado ao cliente e produto especificado
        item = get_object_or_404(Carrinho, cliente=cliente, produto_id=produto_id)
        item.delete()  # Remove o item do carrinho
    return redirect('/vetor5/carrinho/')  # Redireciona de volta para a página do carrinho

def historico_cliente(request):
    pass

def login_cliente(request):
    return render(request, 'login_cliente.html')

def valida_login_cliente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        cliente = Cliente.objects.filter(email=email, senha=senha).first()

        if cliente:
            request.session['cliente'] = cliente.id
            return redirect('/vetor5/cliente/')
        else:
            return redirect('/vetor5/login_cliente/?status=1')
    return render(request, 'login.html')


def cadastro_cliente(request):
    return render(request, 'cadastro_cliente.html')

def valida_cadastro_cliente(request):
   nome =  request.POST.get('nome')
   senha = request.POST.get('senha')
   email = request.POST.get('email')
   foto = request.POST.get('foto')
   
   cliente = Cliente.objects.filter(email = email, nome = nome, senha = senha, foto = foto)
   #---------------------aqui----------------------
   if len(nome.strip()) == 0 or len(email.strip()) == 0:
       return redirect('/SITE_ADMISSAO/logado/?status=9')
   
   if len(senha) < 8:
       return redirect('/SITE_ADMISSAO/logado/?status=10')
   
   if len(cliente) > 0:
       return redirect('/SITE_ADMISSAO/logado/?status=11')
   
   try:
       #senha = sha256(senha.encode()).hexdigest
       cliente = Cliente(nome = nome, senha = senha, email = email, foto = foto)
       cliente.save()
       return redirect('/vetor5/login_cliente/?status=1')
   except:
       return redirect('/SITE_ADMISSAO/cadastro/?status=4')
       #return HttpResponse(f"{nome}, {senha}, {email}")

def valida_cadastro_gerente_cliente(request):
   nome =  request.POST.get('nome')
   senha = request.POST.get('senha')
   email = request.POST.get('email')
   foto = request.POST.get('foto')
   
   cliente = Cliente.objects.filter(email = email, nome = nome, senha = senha, foto = foto)
   #---------------------aqui----------------------
   if len(nome.strip()) == 0 or len(email.strip()) == 0:
       return redirect('/SITE_ADMISSAO/logado/?status=9')
   
   if len(senha) < 8:
       return redirect('/SITE_ADMISSAO/logado/?status=10')
   
   if len(cliente) > 0:
       return redirect('/SITE_ADMISSAO/logado/?status=11')
   
   try:
       #senha = sha256(senha.encode()).hexdigest
       cliente = Cliente(nome = nome, senha = senha, email = email, foto = foto)
       cliente.save()
       return redirect('/vetor5/gerente/?status=1')
   except:
       return redirect('/SITE_ADMISSAO/cadastro/?status=4')
       #return HttpResponse(f"{nome}, {senha}, {email}")

def empresa(request):
    if 'empresa' in request.session:
        empresa_id = request.session['empresa']
        empresa = get_object_or_404(Empresas, id=empresa_id)
        pedidos = Pedido_empresa.objects.filter(empresa=empresa)
        produtos = Produtos.objects.all()

        # Passa os dados para o contexto
        return render(request, 'empresa.html', {'empresa': empresa, 'pedidos': pedidos, 'produtos':produtos})
    else:
        return redirect('/vetor5/login_empresa/?status=2')


def excluir_usuario(request, id):
    cliente = Cliente.objects.get(id = id).delete()
    return redirect('/vetor5/nossos_clientes/')


def historico_empresa(request):
    pass

def marca(request):
    if request.method == 'POST':
        form = MarcaProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vetor5/marca/')  # Redirecionar para uma página de sucesso
    else:
        form = MarcaProdutoForm()
    marcas = Marca_produto.objects.all()
    return render(request, 'marca.html', {'form': form, 'marcas': marcas})

def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vetor5/categoria/')  # Redireciona para a página de listagem de categorias
    else:
        form = CategoriaProdutoForm()
        categorias = Categoria_produto.objects.all()

    return render(request, 'categoria.html', {'form': form, 'categorias': categorias})

def criar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vetor5/fornecedor/')  # Redireciona para a lista de fornecedores após salvar
    else:
        form = FornecedorForm()
        fornecedor = Fornecedor.objects.all()
    return render(request, 'fornecedor.html', {'form': form, 'fornecedores':fornecedor})  

def eliminar_fornecedor(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    fornecedor.delete()
    return redirect('/vetor5/fornecedor/')

def categoria(request):
    categorias = Categoria_produto.objects.all()
    return render(request, 'categoria.html', {'categorias': categorias})

def minha_categoria(request):
    return render(request, 'adicionar_categoria.html')

def fornecedor(request):
    return render(request, 'fornecedor.html')

def login_empresa(request):
    return render(request, 'login_empresa.html')

def valida_login_empresa(request):
    status = request.POST.get('status')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    #senha = sha256(senha.encode()).hexdigest()
    
    empresa = Empresas.objects.filter(email = email, senha = senha) # tras 
    # do banco de dadosalguem onde o email senha igual a esse email, e senha que seja igual a essa senha...
    
    
    if len(empresa) == 0:
        return redirect('/vetor5/login_empresa/?status=1')
    
    if len(empresa) > 0:
        request.session['empresa'] = empresa[0].id
        return redirect('/vetor5/empresa/')


def cadastro_empresa(request):
   return render(request, 'cadastro_empresa.html')

def valida_cadastro_empresa(request):
   nome =  request.POST.get('nome')
   senha = request.POST.get('senha')
   email = request.POST.get('email')
   foto = request.POST.get('foto')
   nif = request.POST.get('nif')
   
   empresa = Empresas.objects.filter(email = email, nome = nome, senha = senha, foto = foto, nif = nif)
   #---------------------aqui----------------------
   if len(nome.strip()) == 0 or len(email.strip()) == 0:
       return redirect('/SITE_ADMISSAO/logado/?status=9')
   
   if len(senha) < 8:
       return redirect('/vetor5/login/?status=10')
   
   if len(empresa) > 0:
       return redirect('/vetor5/login/logado/?status=11')
   
   try:
       #senha = sha256(senha.encode()).hexdigest
       empresa = Empresas(nome = nome, senha = senha, email = email, foto = foto, nif = nif)
       empresa.save()
       return redirect('/vetor5/login_cliente/?status=1')
   except:
       return redirect('/vetor5/login/?status=4')
       #return HttpResponse(f"{nome}, {senha}, {email}")


def produtos_detalhe(request, produto_id):
    produto = get_object_or_404(Produtos, id=produto_id)
    return render(request, 'produtos_detalhe.html', {'produto': produto})

def produto_detalhe(request, produto_id):
    if 'cliente' in request.session:
        produto = get_object_or_404(Produtos, id=produto_id)
        return render(request, 'produto_detalhe.html', {'produto': produto})
    else:
        return HttpResponse("Voce nao esta autenticado para esta pagina")

def avaliar_produto(request):
    if 'cliente' in request.session:
        nome =  request.POST.get('nome')
        email = request.POST.get('email')
        avaliacao  = request.POST.get('avaliacao')
        
        avalia = Avaliacao(nome = nome, email = email, avaliacao = avaliacao)
        avalia.save()
        return HttpResponse("Mensagem enviada")
    else:
        return HttpResponse("Voce nao esta autenticado para esta pagina")
    
def cadastro_produto(request):
    return render(request, 'cadastro_produto.html')

from django.shortcuts import render, redirect
from .forms import ProdutoForm

from django.shortcuts import render, redirect
from .forms import ProdutoForm
from .models import Marca_produto, Categoria_produto, Condicao, Fornecedor

def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Salva os dados no banco de dados
            return redirect('/vetor5/adicionar_produto/')  # Altere 'pagina_de_sucesso' para a rota desejada
    else:
        form = ProdutoForm()
    
    marcas = Marca_produto.objects.all()
    categorias = Categoria_produto.objects.all()
    condicoes = Condicao.objects.all()
    fornecedores = Fornecedor.objects.all()
    
    context = {
        'form': form,
        'marcas': marcas,
        'categorias': categorias,
        'condicoes': condicoes,
        'fornecedores': fornecedores,
    }
    
    return render(request, 'cadastro_produto.html', context)

def contacto_cliente(request):
    if 'cliente' in request.session:
        cliente_id = request.session['cliente']
        cliente = Cliente.objects.get(id=cliente_id)
        produto = Produtos.objects.all()
        categoria = Categoria_produto.objects.all()
        return render(request, 'contacto_cliente.html', {'cliente':cliente, 'produto':produto, 'categoria':categoria})
    else:
        return HttpResponse("Você não está autenticado para acessar esta página.")


def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produtos, id=produto_id)  # Verifica se o produto existe
    cliente_id = request.session.get('cliente')

    if not cliente_id:
        return redirect('/vetor5/login_cliente/?status=2')  # Redireciona para a página de login se não estiver logado

    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Obtém ou cria o carrinho do cliente
    carrinho, created = Carrinho.objects.get_or_create(cliente=cliente)

    # Verifica se o produto já está no carrinho
    item_carrinho, item_created = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)

    if not item_created:
        # Se o item já estiver no carrinho, apenas atualize a quantidade
        item_carrinho.quantidade += 1
    item_carrinho.save()

    return redirect('/vetor5/cliente/')

from django.shortcuts import render, redirect
from .forms import ClienteForm

def adicionar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Salva os dados no banco de dados
            return redirect('/vetor5/gerente/')  # Altere 'pagina_de_sucesso' para a rota desejada
    else:
        form = ClienteForm()
    
    return render(request, 'adicionar_cliente.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import EmpresaForm

def adicionar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Salva os dados no banco de dados
            return redirect('/vetor5/gerente/')  # Altere 'pagina_de_sucesso' para a rota desejada
    else:
        form = EmpresaForm()
    
    return render(request, 'adicionar_empresa.html', {'form': form})


def ver_produto(request):
    produtos = Produtos.objects.all()
    return render(request, 'ver_produto.html', {'produtos':produtos})

def produto_cliente(request):
    produtos = Produtos.objects.all()
    return render(request, 'produto_cliente.html', {'produtos':produtos})

def selecionar_produto(request):
    pass


def carrinho(request):
    cliente_id = request.session.get('cliente')
    if not cliente_id:
        return redirect('/vetor5/login_cliente/?status=2')  # Redireciona para a página de login se não estiver logado

    cliente = get_object_or_404(Cliente, id=cliente_id)
    itens = Carrinho.objects.filter(cliente=cliente)
    return render(request, 'carrinho.html', {
        'itens': itens,
        'cliente': cliente
    })


def carrinho_empresa(request):
    empresa_id = request.session.get('empresa')
    if not empresa_id:
        return redirect('/vetor5/login_empresa/?status=2')  # Redireciona para a página de login se não estiver logado

    empresa = get_object_or_404(Empresas, id=empresa_id)
    carrinho, created = Carrinho_empresa.objects.get_or_create(empresa=empresa)
    itens = ItemCarrinho.objects.filter(carrinho_empresa=carrinho)
    
    return render(request, 'carrinho_empresa.html', {
        'itens': itens,
        'empresa': empresa
    })

def detalhes_produto(request):
    pass

def estoque(request):
    pass

def pagamento(request):
    pass

def noticia(request):
    pass

def conta_login_gerente(request):
    return render(request, 'conta_login_gerente.html')




#--------------------------categorias------------------------------#

def motor(request):
    categoria_motor = Categoria_produto.objects.get(nome = 'motor')
    produtos = Produtos.objects.filter(categoria=categoria_motor)
    return render(request, 'motor.html', {'produtos':produtos})

def freio(request):
    categoria_freio = Categoria_produto.objects.get(nome = 'freios')
    produtos = Produtos.objects.filter(categoria=categoria_freio)
    return render(request, 'freio.html',{'produtos':produtos} )

def eletrico(request):
    categoria_eletrico = Categoria_produto.objects.get(nome = 'eletrico')
    produtos = Produtos.objects.filter(categoria=categoria_eletrico)
    return render(request, 'eletrico.html',{'produtos':produtos})

def interior_conforto(request):
    categoria_interior_conforto = Categoria_produto.objects.get(nome = 'interior')
    produtos = Produtos.objects.filter(categoria=categoria_interior_conforto)
    return render(request, 'interior_conforto.html',{'produtos':produtos})

def carroceria(request):
    categoria_carroceria = Categoria_produto.objects.get(nome = 'carroceria')
    produtos = Produtos.objects.filter(categoria=categoria_carroceria)
    return render(request, 'carroceria.html',{'produtos':produtos})

def suspensao(request):
    categoria_suspensao = Categoria_produto.objects.get(nome = 'suspensão')
    produtos = Produtos.objects.filter(categoria=categoria_suspensao)
    return render(request, 'suspensao.html',{'produtos':produtos})

def transmissao(request):
    categoria_transmissao = Categoria_produto.objects.get(nome = 'transmissão')
    produtos = Produtos.objects.filter(categoria=categoria_transmissao)
    return render(request, 'transmissao.html',{'produtos':produtos})


#------------------------comprar------------------------------


def pedido_confirmado(request):
    return render(request, 'pedido.html')



def sair(request):
    request.session.flush()
    return redirect(request.META.get('HTTP_REFERER', '/'))



from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Fatura, Cliente

def listar_faturas(request):
    cliente_id = request.session.get('cliente')
    if not cliente_id:
        return HttpResponse("Cliente não encontrado na sessão.", status=404)

    cliente = Cliente.objects.get(id=cliente_id)
    faturas = Fatura.objects.filter(cliente=cliente)

    return render(request, 'listar_faturas.html', {'cliente': cliente, 'faturas': faturas})

def lista_estoque(request):
    estoques = Produtos.objects.all()
    return render(request, 'estoque.html', {'estoques': estoques})


def eliminar_estoque(request, id):
    if request.method == 'POST':
        estoque = get_object_or_404(Produtos, id=id)
        estoque.delete()
        return redirect('/vetor5/estoque/')
        return redirect('lista_estoque')  # Ajuste o nome da URL de redirecionamento conforme necessário

    # Se não for um POST, redireciona para a lista de estoque
    return redirect('/vetor5/estoque/')


def pesquisar(request):
    nome_filtrar = request.GET.get('mome_filtrar')

    if nome_filtrar:
        produtos = Produtos.objects.filter(nome__icontains=nome_filtrar)
    else:
        produtos = Produtos.objects.all()  # Ajuste conforme o seu modelo
    return render(request, 'ver_produto.html', {'produtos': produtos})


def pesquisare(request):
    nome_filtrar = request.GET.get('mome_filtrar')

    if nome_filtrar:
        produtos = Produtos.objects.filter(nome__icontains=nome_filtrar)
    else:
        produtos = Produtos.objects.all()  # Ajuste conforme o seu modelo
    return render(request, 'estoque.html', {'produtos': produtos})


def pesquisar_ver(request):
    nome_filtrar = request.GET.get('nome_produto')

    if nome_filtrar:
        produtos = Produtos.objects.filter(nome__icontains=nome_filtrar)
    else:
        produtos = Produtos.objects.all()  # Ajuste conforme o seu modelo
    return render(request, 'ver_produto.html', {'produtos': produtos})

def pesquisar_cliente(request):
    nome_filtrar = request.GET.get('mome_cliente')

    if nome_filtrar:
        produtos = Produtos.objects.filter(nome__icontains=nome_filtrar)
    else:
        produtos = Produtos.objects.all()  # Ajuste conforme o seu modelo
    return render(request, 'cliente.html', {'produtos': produtos})


def editar_perfil(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redireciona para a página de perfil ou outra página desejada
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'editar_perfil.html', {'form': form, 'cliente': cliente})

def ver_fatura(request, fatura_id):
    fatura = get_object_or_404(Fatura, id=fatura_id)
    return render(request, 'factura.html', {'fatura': fatura, 'created': True})

def listar_faturas(request):
    if 'empresa' in request.session:
        cliente_id = request.session['empresa']
        cliente = get_object_or_404(Empresas, id=cliente_id)
        
        # Filtra faturas relacionadas ao cliente
        faturas = Fatura.objects.all()
        produtos = Produtos.objects.all()
        
        return render(request, 'factura.html', {'faturas': faturas, 'cliente': cliente, 'produtos':produtos})
    else:
        return HttpResponse("Você não está autenticado para acessar esta página.")

def sucesso(request, fatura_id):
    fatura = get_object_or_404(Fatura, id=fatura_id)
    return render(request, 'sucesso.html', {'fatura': fatura})


def listar_faturas(request):
    cliente_id = request.session.get('cliente')
    if not cliente_id:
        return redirect('/vetor5/login_cliente/?status=2')  # Redireciona para a página de login se não estiver logado

    cliente = get_object_or_404(Cliente, id=cliente_id)
    itens = Pedido.objects.filter(usuario=cliente)
    return render(request, 'factura.html', {
        'itens': itens,
        'cliente': cliente
    })

def listar_faturas_empresas(request):
    cliente_id = request.session.get('empresa')
    if not cliente_id:
        return redirect('/vetor5/login_cliente/?status=2')  # Redireciona para a página de login se não estiver logado

    cliente = get_object_or_404(Empresas, id=cliente_id)
    itens = Pedido_empresa.objects.filter(empresa=cliente)
    return render(request, 'listar_faturas.html', {
        'itens': itens,
        'cliente': cliente
    })

def pedido_empresa_gerente(request):
    cliente_id = request.session.get('gerente')
    if not cliente_id:
        return redirect('/vetor5/login_cliente/?status=2')  # Redireciona para a página de login se não estiver logado

    cliente = get_object_or_404(Empresas, id=cliente_id)
    itens = Pedido_empresa.objects.filter(empresa=cliente)
    return render(request, 'pedido_empresa_gerente.html', {
        'itens': itens,
        'cliente': cliente
    })


def pedido_cliente_gerente(request):
    cliente_id = request.session.get('gerente')
    if not cliente_id:
        return redirect('/vetor5/login_cliente/?status=2')  # Redireciona para a página de login se não estiver logado

    cliente = get_object_or_404(Cliente, id=cliente_id)
    itens = Pedido.objects.filter(usuario=cliente)
    
    return render(request, 'pedido_cliente_gerente.html', {
        'itens': itens,
        'cliente': cliente
    })





def sucesso(request, fatura_id):
    fatura = get_object_or_404(Fatura, id=fatura_id)
    return render(request, 'sucesso.html', {'fatura': fatura})





def finalizar_compra(request):
    try:
        cliente_id = request.session.get('cliente')
        if not cliente_id:
            return HttpResponse("Cliente não encontrado na sessão.", status=404)

        cliente = Cliente.objects.get(id=cliente_id)
        carrinho = Carrinho.objects.get(cliente=cliente)
        itens = ItemCarrinho.objects.filter(carrinho=carrinho)

        subtotal = sum(item.subtotal() for item in itens)
        total = subtotal  

        if request.method == 'POST':
            form = PedidoForm(request.POST)
            if form.is_valid():
                pedido = form.save(commit=False)
                pedido.usuario = cliente
                pedido.save()

                for item in itens:
                    ItemPedido.objects.create(
                        pedido=pedido,
                        produto=item.produto,
                        quantidade=item.quantidade
                    )

                # REDIRECIONAR para pagamento APÓS CRIAR O PEDIDO
                return redirect('pagamento', pedido_id=pedido.id)  
        else:
            form = PedidoForm()

        return render(request, 'pedido.html', {
            'form': form,
            'itens': itens,
            'carrinho': carrinho,
            'subtotal': subtotal,
            'total': total
        })
    
    except Cliente.DoesNotExist:
        return HttpResponse("Cliente não encontrado.", status=404)
    except Carrinho.DoesNotExist:
        return HttpResponse("Carrinho não encontrado.", status=404)  



from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Fatura, Cliente, Pedido, Produtos, ItemPedido, Carrinho
from .forms import PedidoForm 
from django.core.files.storage import FileSystemStorage  
from django.utils import timezone  





def pagamento_view(request, pedido_id):
    if request.method == 'POST':
        cliente_id = request.session.get('cliente')
        if not cliente_id:
            return HttpResponse("Cliente não encontrado na sessão.", status=404)

        comprovante = request.FILES.get('comprovativo') 

        if comprovante:
            fs = FileSystemStorage()
            filename = fs.save(comprovante.name, comprovante)
            file_path = fs.path(filename)
            
            try:
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfFileReader(f)
                    num_pages = reader.numPages
                    text = ""
                    for page in range(num_pages):
                        text += reader.getPage(page).extractText()
                
                if any(word in text for word in ["BAI", "Atlântico", "BPC"]):
                    file_url = fs.url(filename)
                    print(f"Pagamento recebido, comprovante: {file_url}")

                    transacao_realizada = True  # Alterar lógica conforme necessário
                    if transacao_realizada:
                        try:
                            pedido = Pedido.objects.get(pk=pedido_id)
                            cliente = Cliente.objects.get(pk=cliente_id)
                            fatura = Fatura.objects.create(
                                cliente=cliente,
                                pedido=pedido,
                                valor_total=pedido.total(),
                                data_emissao=timezone.now()
                            )
                            
                            carrinho = Carrinho.objects.get(cliente=cliente) 
                            carrinho.produtos.clear()  
                            
                            return redirect('/vetor5/faturas', fatura_id=fatura.id)
                        except Exception as e:
                            return HttpResponse(f"Erro ao criar a fatura: {e}", status=500)
                else:
                    return HttpResponse("O comprovativo é inválido.", status=400)

            except Exception as e:
                return HttpResponse(f"Erro ao ler o comprovativo: {e}", status=500)


    pedido = get_object_or_404(Pedido, pk=pedido_id) 
    iban = Iban.objects.all()
    return render(request, 'pagamento.html', {'pedido': pedido, 'ibans': iban})

def ver_produto_empresa(request):
    produtos = Produtos.objects.all()
    return render(request, 'ver_produto_empresa.html', {'produtos':produtos})


def adicionar_ao_carrinho_empresa(request, produto_id):
    produto = get_object_or_404(Produtos, id=produto_id)
    empresa_id = request.session.get('empresa')  # ou outro identificador de sessão

    if not empresa_id:
        return redirect('/vetor5/login_empresa/?status=2')

    empresa = get_object_or_404(Empresas, id=empresa_id)
    carrinho, created = Carrinho_empresa.objects.get_or_create(empresa=empresa)
    
    item_carrinho, item_created = ItemCarrinho.objects.get_or_create(carrinho_empresa=carrinho, produto=produto)
    
    if not item_created:
        item_carrinho.quantidade += 1
    item_carrinho.save()

    return redirect('/vetor5/empresa/')



def finalizar_compra_empresa(request):
    try:
        empresa_id = request.session.get('empresa')
        if not empresa_id:
            return redirect('/vetor5/login_empresa/?status=2')  # Redireciona para a página de login se não estiver logado

        empresa = Empresas.objects.get(id=empresa_id)
        carrinho = Carrinho_empresa.objects.get(empresa=empresa)
        itens = ItemCarrinho.objects.filter(carrinho_empresa=carrinho)

        if not itens:
            return redirect('/vetor5/pagamento/?status=3')  # Carrinho vazio

        subtotal = sum(item.subtotal() for item in itens)
        total = subtotal 

        if request.method == 'POST':
            form = PedidoEmpresaForm(request.POST)
            if form.is_valid():
                pedido = form.save(commit=False)
                pedido.empresa = empresa
                pedido.data = timezone.now()
                pedido.status = 'Pendente'
                pedido.save()

                for item in itens:
                    ItemPedidoEmpresa.objects.create(
                        pedido=pedido,
                        produto=item.produto,
                        quantidade=item.quantidade,
                        preco=item.produto.preco
                    )
                    item.delete()  # Remove o item do carrinho após a compra

                # Criar a fatura associada à empresa
                Fatura.objects.create(
                    empresa=empresa,
                    pedido=pedido,
                    valor_total=pedido.total(),
                    data_emissao=timezone.now()
                )

                # Verifique se o pedido foi salvo corretamente e se possui um ID
                if pedido.id:
                    return redirect('pagamento_empresa', pedido_id=pedido.id)
                else:
                    return HttpResponse("Erro ao salvar o pedido.", status=500)
        else:
            form = PedidoEmpresaForm()

        return render(request, 'pagamento_empresa.html', {
            'form': form,
            'itens': itens,
            'carrinho': carrinho,
            'subtotal': subtotal,
            'total': total
        })

    except Empresas.DoesNotExist:
        return HttpResponse("Empresa não encontrada.", status=404)
    except Carrinho_empresa.DoesNotExist:
        return HttpResponse("Carrinho não encontrado.", status=404)
    except Exception as e:
        # Captura qualquer outra exceção não prevista
        return HttpResponse(f"Erro inesperado: {str(e)}", status=500)


def pagamentos_empresa(request, pedido_id):
    empresa_id = request.session.get('empresa')
    if not empresa_id:
        return redirect('/vetor5/login_empresa/?status=2')  # Redireciona para a página de login se não estiver logado

    empresa = get_object_or_404(Empresas, id=empresa_id)
    faturas = Fatura.objects.filter(empresa=empresa)  # Ajuste o filtro conforme seu modelo

    if request.method == 'POST':
        comprovante = request.FILES.get('comprovativo')
        if comprovante:
            fs = FileSystemStorage()
            filename = fs.save(comprovante.name, comprovante)
            file_path = fs.path(filename)
            
            try:
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfFileReader(f)
                    text = ""
                    for page in range(reader.numPages):
                        text += reader.getPage(page).extractText()
                
                if any(word in text for word in ["BAI", "Atlântico", "BPC"]):
                    file_url = fs.url(filename)
                    print(f"Pagamento recebido, comprovante: {file_url}")

                    try:
                        pedido = get_object_or_404(Pedido_empresa, id=pedido_id, empresa=empresa)
                        fatura = Fatura.objects.create(
                            empresa=empresa,
                            pedido=pedido,
                            valor_total=pedido.total(),
                            data_emissao=timezone.now()
                        )

                        # Limpar o carrinho
                        carrinho = Carrinho_empresa.objects.get(empresa=empresa)  # Supondo que exista um modelo de Carrinho_empresa
                        carrinho.itemcarrinho_set.all().delete()  # Remove todos os itens do carrinho
                        
                        return redirect('/vetor5/faturas', fatura_id=fatura.id)  # Corrigir URL para redirecionar adequadamente
                    except Exception as e:
                        return HttpResponse(f"Erro ao criar a fatura: {e}", status=500)
                else:
                    return HttpResponse("O comprovativo é inválido.", status=400)

            except Exception as e:
                return HttpResponse(f"Erro ao ler o comprovativo: {e}", status=500)

    return render(request, 'pagamento_empresa.html', {'empresa': empresa, 'faturas': faturas})


def perfil_empresa(request):
    empresa_id = request.session.get('empresa')

    if not empresa_id:
        return redirect('pagina_inicial')  # Substitua 'pagina_inicial' pelo nome da URL desejada

    empresa = get_object_or_404(Empresas, id=empresa_id)

    return render(request, 'perfil_empresa.html', {'empresa': empresa})

def contacto_empresa(request):
    
    empresa_id = request.session.get('empresa')
    if not empresa_id:
        return redirect('pagina_inicial')

    empresa = get_object_or_404(Empresas, id=empresa_id) 

    return render(request, 'contacto_empresa.html', {'empresa': empresa})

def contato_view(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vector5/contacto_empresa')  # Redireciona para uma página de sucesso ou outra view
    else:
        form = ContatoForm()
    
    return render(request, 'contacto_empresa.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Pedido, Fatura, ItemPedido

@login_required
def gerar_fatura(request, pedido_id):
    if 'cliente' in request.session:
        cliente_id = request.session['cliente']
        cliente = get_object_or_404(Cliente, id=cliente_id)
        
        # Verificar se o pedido pertence ao cliente autenticado
        pedido = get_object_or_404(Pedido, id=pedido_id, usuario=cliente)
        
        # Calcular o valor total e criar a fatura (se necessário)
        itens_pedido = pedido.item_pedido_set.all()
        valor_total = sum(item.subtotal() for item in itens_pedido)
        
        # Adicione o código para criar a fatura, se necessário
        fatura = Fatura.objects.create(
            cliente=cliente,
            pedido=pedido,
            valor_total=valor_total
        )

        # Renderizar o template com os dados do pedido
        return render(request, 'lista_facturas.html', {'pedido': pedido, 'itens_pedido': itens_pedido, 'valor_total': valor_total, 'faturas':fatura})
    else:
        return HttpResponse("Você não está autenticado para acessar esta página.")

def lista_faturas(request):
    faturas = Fatura.objects.all()
    return render(request, 'lista_faturas.html', {'faturas': faturas})



def detalhe_produto(request, produto_id):
    produto = get_object_or_404(Produtos, id=produto_id)
    return render(request, 'detalhe_produto.html', {'produto': produto})

from django.contrib import messages
def eliminar_fatura(request, fatura_id):
    if request.method == 'POST':
        fatura = get_object_or_404(Fatura, id=fatura_id)
        fatura.delete()
        messages.success(request, 'Fatura excluída com sucesso!')
    return redirect('listar_faturas')  # Redireciona para a lista de faturas

def visualizar_fatura(request, fatura_id):
    fatura = get_object_or_404(Fatura, id=fatura_id)
    return render(request, 'sucesso.html', {'fatura': fatura})


def clientes_cadastrados(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes_cadastrados.html', {'clientes': clientes})


def eliminar_cliente(request, cliente_id):
    # Obtém o cliente com base no ID fornecido
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    # Exclui o cliente
    cliente.delete()
    
    # Redireciona para a lista de clientes após a eliminação
    return redirect('/vetor5/clientes_cadastrados/') 

def visao_geral(request):
    produto = Produtos.objects.all()
    categoria = Categoria_produto.objects.all()
    return render(request, 'visao_geral.html', {'produto':produto, 'categoria':categoria})


def suporte(request):
    return render(request, 'suporte.html')


from django.shortcuts import render, redirect
from .forms import TicketForm

def enviar_suporte(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vetor5/suporte')  # Redireciona para uma página de sucesso
    else:
        form = TicketForm()
    
    return render(request, 'suporte.html', {'form': form})

from .models import Ticket, Gerente
def tickets_gerente(request):
    if 'gerente' not in request.session:
        return redirect('/vetor5/login_gerente/?status=2')  # Redireciona para a página de login se não estiver logado
    
    gerente_id = request.session['gerente']
    try:
        gerente = Gerente.objects.get(id=gerente_id)
    except Gerente.DoesNotExist:
        return redirect('/vetor5/login_gerente/?status=2')  # Redireciona se o gerente não existir
    
    # Obtém todos os tickets, ordenados por data de criação
    tickets = Ticket.objects.all().order_by('-data_criacao')
    
    return render(request, 'suporte_gerente.html', {'tickets': tickets, 'gerente': gerente})

def ticket_detalhes(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, 'suporte_gerente.html', {'ticket': ticket})

def atualizar_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    if request.method == 'POST':
        # Aqui você pode implementar a lógica para atualizar o ticket
        # Por exemplo, mudar o status
        ticket.status = request.POST.get('status', ticket.status)
        ticket.save()
        return redirect('tickets_gerente')  # Redireciona de volta para a lista de tickets
    return render(request, 'suporte_gerente.html', {'ticket': ticket})