from django.shortcuts import render
from django.shortcuts import redirect
from .models import Gerente, Cliente, Empresas, Marca_produto, Categoria_produto
from .models import Condicao, Fornecedor, Produtos, Carrinho_empresa, Iban
from .forms import MarcaProdutoForm
from .models import Categoria_produto, Estoque, Noticia,  Marca_index, Video, ItemPedidoEmpresa
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
        
        try:
            # Obtém o cliente da base de dados
            cliente = Cliente.objects.get(id=cliente_id)
            
            # Obtém todos os produtos e categorias
            produto = Produtos.objects.all()
            categoria = Categoria_produto.objects.all()

            # Obtém o carrinho do cliente, cria um novo se não existir
            carrinho, created = Carrinho.objects.get_or_create(cliente=cliente)
            itens = ItemCarrinho.objects.filter(carrinho=carrinho)

            # Calcula subtotal e total
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

            return render(request, 'cliente.html', {
                'cliente': cliente,
                'produto': produto,
                'categoria': categoria,
                'itens': itens,
                'carrinho': carrinho,
                'form': form,
                'subtotal': subtotal,
                'total': total
            })

        except Cliente.DoesNotExist:
            return HttpResponse("Cliente não encontrado.", status=404)
    else:
        return HttpResponse("Você não está autenticado para acessar esta página.")


def remover_do_carrinho(request, produto_id):
    if 'cliente' in request.session:
        cliente_id = request.session['cliente']
        cliente = get_object_or_404(Cliente, id=cliente_id)
        carrinho = get_object_or_404(Carrinho, cliente=cliente)

        # Busca o ItemCarrinho associado ao cliente, ao carrinho e ao produto especificado
        item = get_object_or_404(ItemCarrinho, carrinho=carrinho, produto_id=produto_id)
        item.delete()  # Remove o item do carrinho

    return redirect('/vetor5/carrinho/')  # Redireciona de volta para a página do carrinho


def historico_cliente(request):
    pass

def login_cliente(request):
    status = request.GET.get('status')
    return render(request, 'login_cliente.html', {'status':status})

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
    status = request.GET.get('status')
    return render(request, 'cadastro_cliente.html', {'status':status})

def valida_cadastro_cliente(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    email = request.POST.get('email')

    print(f"Nome: {nome}, Senha: {senha}, Email: {email}")

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        print("Erro: Nome ou Email em branco.")
        return redirect('/vetor5/cadastro_cliente/?status=9')

    if len(senha) < 8:
        print("Erro: Senha menor que 8 caracteres.")
        return redirect('/vetor5/cadastro_cliente/?status=10')

    cliente = Cliente.objects.filter(email=email, nome=nome).exists()

    if cliente:
        print("Erro: Cliente já cadastrado.")
        return redirect('/vetor5/cadastro_cliente/?status=11')

    try:
        cliente = Cliente(nome=nome, senha=senha, email=email)
        cliente.save()
        print("Cliente salvo com sucesso.")
        return redirect('/vetor5/cadastro_cliente/?status=1')
    except Exception as e:
        print(f"Erro ao salvar cliente: {e}")  # Isto irá mostrar o erro específico
        return redirect('/vetor5/cadastro_cliente/?status=4')

def valida_cadastro_gerente_cliente(request):
   nome =  request.POST.get('nome')
   senha = request.POST.get('senha')
   email = request.POST.get('email')
   
   
   cliente = Cliente.objects.filter(email = email, nome = nome, senha = senha)
   #---------------------aqui----------------------
   if len(nome.strip()) == 0 or len(email.strip()) == 0:
       return redirect('/SITE_ADMISSAO/logado/?status=9')
   
   if len(senha) < 8:
       return redirect('/SITE_ADMISSAO/logado/?status=10')
   
   if len(cliente) > 0:
       return redirect('/SITE_ADMISSAO/logado/?status=11')
   
   try:
       #senha = sha256(senha.encode()).hexdigest
       cliente = Cliente(nome = nome, senha = senha, email = email)
       cliente.save()
       return redirect('/vetor5/gerente/?status=1')
   except:
       return redirect('/SITE_ADMISSAO/cadastro/?status=4')
       #return HttpResponse(f"{nome}, {senha}, {email}")

def empresa(request):
    if 'empresa' in request.session:
        empresa_id = request.session['empresa']
        
        try:
            # Obtém a empresa da base de dados
            empresa = Empresas.objects.get(id=empresa_id)
            
            # Obtém todos os produtos
            produtos = Produtos.objects.all()

            # Obtém o carrinho da empresa, cria um novo se não existir
            carrinho_empresa, created = Carrinho_empresa.objects.get_or_create(empresa=empresa)
            itens = ItemCarrinho.objects.filter(carrinho_empresa=carrinho_empresa)

            # Calcula subtotal e total
            subtotal = sum(item.subtotal() for item in itens)
            total = subtotal

            if request.method == 'POST':
                form = PedidoForm(request.POST)
                if form.is_valid():
                    pedido = form.save(commit=False)
                    pedido.empresa = empresa
                    pedido.save()

                    for item in itens:
                        ItemPedidoEmpresa.objects.create(
                            pedido=pedido,
                            produto=item.produto,
                            quantidade=item.quantidade
                        )

                    # REDIRECIONAR para pagamento APÓS CRIAR O PEDIDO
                    return redirect('pagamento_empresa', pedido_id=pedido.id)
            else:
                form = PedidoForm()

            return render(request, 'empresa.html', {
                'empresa': empresa,
                'produto': produtos,
                'carrinho_empresa': carrinho_empresa,
                'itens': itens,
                'form': form,
                'subtotal': subtotal,
                'total': total
            })

        except Empresas.DoesNotExist:
            return HttpResponse("Empresa não encontrada.", status=404)
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
    status = request.GET.get('status')
    return render(request, 'cadastro_empresa.html', {'status':status})

def valida_cadastro_empresa(request):
   nome =  request.POST.get('nome')
   senha = request.POST.get('senha')
   email = request.POST.get('email')
   nif = request.POST.get('nif')
   
   empresa = Empresas.objects.filter(email = email, nome = nome, senha = senha, nif = nif)
   #---------------------aqui----------------------
   if len(nome.strip()) == 0 or len(email.strip()) == 0:
       return redirect('/vetor5/cadastro_empresa/?status=9')
   
   if len(senha) < 8:
       return redirect('/vetor5/cadastro_empresa/?status=10')
   
   if len(empresa) > 0:
       return redirect('/vetor5/cadastro_empresa/?status=11')
   
   try:
       #senha = sha256(senha.encode()).hexdigest
       empresa = Empresas(nome = nome, senha = senha, email = email, nif = nif)
       empresa.save()
       return redirect('/vetor5/login_empresa/?status=1')
   except:
       return redirect('/vetor5/cadastro_empresa/?status=4')
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
            print("Formulário é válido")
            form.save()
            return redirect('/vetor5/adicionar_produto/')  # Redireciona após salvar o produto
        else:
            print("Formulário não é válido")
            print(form.errors)  # Adicione isso para ver os erros do formulário
    else:
        form = ProdutoForm()

    # Consultando as tabelas relacionadas para popular os campos do formulário
    marcas = Marca_produto.objects.all()
    categorias = Categoria_produto.objects.all()
    condicoes = Condicao.objects.all()
    fornecedores = Fornecedor.objects.all()

    # Contexto a ser enviado para o template
    context = {
        'form': form,
        'marcas': marcas,
        'categorias': categorias,
        'condicoes': condicoes,
        'fornecedores': fornecedores,
    }

    # Renderiza o template com o formulário e os dados adicionais
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
    if 'cliente' in request.session:
        cliente_id = request.session['cliente']
        
        try:
            # Obtém o cliente da base de dados
            cliente = Cliente.objects.get(id=cliente_id)
            
            # Obtém todos os produtos e categorias
            produto = Produtos.objects.all()
            categoria = Categoria_produto.objects.all()

            # Obtém o carrinho do cliente, cria um novo se não existir
            carrinho, created = Carrinho.objects.get_or_create(cliente=cliente)
            itens = ItemCarrinho.objects.filter(carrinho=carrinho)

            # Calcula subtotal e total
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

            return render(request, 'carrinho.html', {
                'cliente': cliente,
                'produto': produto,
                'categoria': categoria,
                'itens': itens,
                'carrinho': carrinho,
                'form': form,
                'subtotal': subtotal,
                'total': total
            })

        except Cliente.DoesNotExist:
            return HttpResponse("Cliente não encontrado.", status=404)
    else:
        return HttpResponse("Você não está autenticado para acessar esta página.")



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
    return render(request, 'motor.html', {'categoria':categoria_motor, 'produtos':produtos})

def freio(request):
    categoria_freio = Categoria_produto.objects.get(nome = 'freios')
    produtos = Produtos.objects.filter(categoria=categoria_freio)
    return render(request, 'freio.html',{'produtos':produtos} )

def eletrico(request):
    categoria_eletrico = Categoria_produto.objects.get(nome = 'sistema elétrico')
    produtos = Produtos.objects.filter(categoria=categoria_eletrico)
    return render(request, 'eletrico.html',{'categoria':categoria_eletrico, 'produtos':produtos})

def interior_conforto(request):
    categoria_interior_conforto = Categoria_produto.objects.get(nome = 'Interior')
    produtos = Produtos.objects.filter(categoria=categoria_interior_conforto)
    return render(request, 'interior_conforto.html',{'categoria':categoria_interior_conforto, 'produtos':produtos})

def carroceria(request):
    categoria_carroceria = Categoria_produto.objects.get(nome = 'carroceria')
    produtos = Produtos.objects.filter(categoria=categoria_carroceria)
    return render(request, 'carroceria.html',{'produtos':produtos})

def suspensao(request):
    categoria_suspensao = Categoria_produto.objects.get(nome = 'direção e suspensão')
    produtos = Produtos.objects.filter(categoria=categoria_suspensao)
    return render(request, 'suspensao.html',{'categoria':categoria_suspensao, 'produtos':produtos})

def transmissao(request):
    categoria_transmissao = Categoria_produto.objects.get(nome = 'transmissão')
    produtos = Produtos.objects.filter(categoria=categoria_transmissao)
    return render(request, 'transmissao.html',{'categoria':produtos})

#-----------------------------------------------
from django.shortcuts import redirect

def interior_cliente(request):
    if 'cliente' not in request.session:
        return redirect('login_url')  # Redireciona para a página de login se o usuário não estiver logado

    cliente_id = request.session['cliente']
    cliente = Cliente.objects.get(id=cliente_id)
    
    categoria_interior = get_object_or_404(Categoria_produto, nome='Interior')
    produtos = Produtos.objects.filter(categoria=categoria_interior)
    return render(request, 'interior_cliente.html', {'produtos': produtos, 'categoria': categoria_interior, 'cliente': cliente})

def motor_cliente(request):
    if 'cliente' not in request.session:
        return redirect('login_url')

    cliente_id = request.session['cliente']
    cliente = Cliente.objects.get(id=cliente_id)

    categoria_motor = get_object_or_404(Categoria_produto, nome='motor')
    produtos = Produtos.objects.filter(categoria=categoria_motor)
    return render(request, 'motor_cliente.html', {'produtos': produtos, 'categoria': categoria_motor, 'cliente': cliente})

def sistema_eletrico_cliente(request):
    if 'cliente' not in request.session:
        return redirect('login_url')

    cliente_id = request.session['cliente']
    cliente = Cliente.objects.get(id=cliente_id)

    categoria_sistema_eletrico = get_object_or_404(Categoria_produto, nome='sistema elétrico')
    produtos = Produtos.objects.filter(categoria=categoria_sistema_eletrico)
    return render(request, 'sistema_eletrico_cliente.html', {'produtos': produtos, 'categoria': categoria_sistema_eletrico, 'cliente': cliente})

def direcao_suspensao_cliente(request):
    if 'cliente' not in request.session:
        return redirect('login_url')

    cliente_id = request.session['cliente']
    cliente = Cliente.objects.get(id=cliente_id)

    categoria_direcao_suspensao = get_object_or_404(Categoria_produto, nome='direção e suspensão')
    produtos = Produtos.objects.filter(categoria=categoria_direcao_suspensao)
    return render(request, 'direcao_suspensao_cliente.html', {'produtos': produtos, 'categoria': categoria_direcao_suspensao, 'cliente': cliente})

#------------------empresas------------------------

def interior_empresa(request):
    if 'empresa' not in request.session:
        return redirect('login_empresa')  # Redireciona para a página de login se a empresa não estiver logada

    empresa_id = request.session['empresa']
    empresa = Empresas.objects.get(id=empresa_id)
    
    categoria_interior = get_object_or_404(Categoria_produto, nome='Interior')
    produtos = Produtos.objects.filter(categoria=categoria_interior)
    return render(request, 'interior_empresa.html', {'produtos': produtos, 'categoria': categoria_interior, 'empresa': empresa})



def motor_empresa(request):
    if 'empresa' not in request.session:
        return redirect('login_empresa')

    empresa_id = request.session['empresa']
    empresa = Empresas.objects.get(id=empresa_id)

    categoria_motor = get_object_or_404(Categoria_produto, nome='motor')
    produtos = Produtos.objects.filter(categoria=categoria_motor)
    return render(request, 'motor_empresa.html', {'produtos': produtos, 'categoria': categoria_motor, 'empresa': empresa})


def sistema_eletrico_empresa(request):
    if 'empresa' not in request.session:
        return redirect('login_empresa')

    empresa_id = request.session['empresa']
    empresa = Empresas.objects.get(id=empresa_id)

    categoria_sistema_eletrico = get_object_or_404(Categoria_produto, nome='sistema elétrico')
    produtos = Produtos.objects.filter(categoria=categoria_sistema_eletrico)
    return render(request, 'sistema_eletrico_empresa.html', {'produtos': produtos, 'categoria': categoria_sistema_eletrico, 'empresa': empresa})


def direcao_suspensao_empresa(request):
    if 'empresa' not in request.session:
        return redirect('login_empresa')

    empresa_id = request.session['empresa']
    empresa = Empresas.objects.get(id=empresa_id)

    categoria_direcao_suspensao = get_object_or_404(Categoria_produto, nome='direção e suspensão')
    produtos = Produtos.objects.filter(categoria=categoria_direcao_suspensao)
    return render(request, 'direcao_suspensao_empresa.html', {'produtos': produtos, 'categoria': categoria_direcao_suspensao, 'empresa': empresa})

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



import cv2
import numpy as np
from django.shortcuts import render
from .models import Produtos

def pesquisar(request):
    nome_filtrar = request.GET.get('nome_filtrar')
    imagem_filtrar = request.FILES.get('imagem_filtrar')

    if nome_filtrar:
        produtos = Produtos.objects.filter(nome__icontains=nome_filtrar)
    elif imagem_filtrar:
        produtos = []
        query_image = cv2.imdecode(np.fromstring(imagem_filtrar.read(), np.uint8), cv2.IMREAD_COLOR)

        for produto in Produtos.objects.all():
            produto_imagem_path = produto.imagem.path
            produto_imagem = cv2.imread(produto_imagem_path)

            # Comparação básica usando histogramas (por exemplo)
            hist_query = cv2.calcHist([query_image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist_produto = cv2.calcHist([produto_imagem], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

            # Comparar as imagens (quanto menor a diferença, mais próximas as imagens)
            diff = cv2.compareHist(hist_query, hist_produto, cv2.HISTCMP_CORREL)
            if diff > 0.7:  # Ajuste o limiar conforme necessário
                produtos.append(produto)
    else:
        produtos = Produtos.objects.all()

    return render(request, 'cliente.html', {'produto': produtos})




def pesquisare(request):
    nome_filtrar = request.GET.get('nome_filtrar')
    imagem_filtrar = request.FILES.get('imagem_filtrar')

    if nome_filtrar:
        produtos = Produtos.objects.filter(nome__icontains=nome_filtrar)
    elif imagem_filtrar:
        produtos = []
        query_image = cv2.imdecode(np.fromstring(imagem_filtrar.read(), np.uint8), cv2.IMREAD_COLOR)

        for produto in Produtos.objects.all():
            produto_imagem_path = produto.imagem.path
            produto_imagem = cv2.imread(produto_imagem_path)

            # Comparação básica usando histogramas (por exemplo)
            hist_query = cv2.calcHist([query_image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist_produto = cv2.calcHist([produto_imagem], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

            # Comparar as imagens (quanto menor a diferença, mais próximas as imagens)
            diff = cv2.compareHist(hist_query, hist_produto, cv2.HISTCMP_CORREL)
            if diff > 0.7:  # Ajuste o limiar conforme necessário
                produtos.append(produto)
    else:
        produtos = Produtos.objects.all()

    return render(request, 'ver_produto.html', {'produtos': produtos})


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
    produto = Produtos.objects.all()
    return render(request, 'pedido_empresa_gerente.html', {
        'itens': itens,
        'cliente': cliente,
        'produto':produto
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



from django.core.mail import send_mail
import PyPDF2
from PyPDF2 import PdfReader  # Substitua PdfFileReader por PdfReader

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
                    reader = PdfReader(f)  # Usando PdfReader em vez de PdfFileReader
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()

                if any(word in text for word in ["BAI", "ATLANTICO", "BPC"]):
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

                            send_mail(
                            'Pedido Recebido',
                            f'Olá {cliente.nome}, seu pedido foi recebido e está sendo processado.',
                            'muquissicarlos@gmail.com',  # Substitua pelo seu email
                            [cliente.email],
                            fail_silently=False,
                        )  

                            return redirect('/vetor5/faturas', fatura_id=fatura.id)
                        except Exception as e:
                            return HttpResponse(f"Erro ao criar a fatura, Nome de usuário e senha não aceitos pelo google, esse dominio precisar estar hospedado! ", status=500)
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
        carrinho = get_object_or_404(Carrinho_empresa, empresa=empresa)

        # Obtém os itens do carrinho
        itens = ItemCarrinho.objects.filter(carrinho_empresa=carrinho)

        if not itens:
            return redirect('/vetor5/pagamento_empresa/?status=3')  # Carrinho vazio

        subtotal = sum(item.subtotal() for item in itens)
        total = subtotal  # Ajuste se você tiver impostos ou outras taxas

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
        return HttpResponse(f"Erro inesperado: {str(e)}", status=500)


def pagamentos_empresa(request, pedido_id):
    empresa_id = request.session.get('empresa')
    if not empresa_id:
        return redirect('/vetor5/login_empresa/?status=2')

    empresa = get_object_or_404(Empresas, id=empresa_id)
    faturas = Fatura.objects.filter(empresa=empresa)

    if request.method == 'POST':
        comprovante = request.FILES.get('comprovativo')
        if comprovante:
            fs = FileSystemStorage()
            filename = fs.save(comprovante.name, comprovante)
            file_path = fs.path(filename)
            
            try:
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f)
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

                        carrinho = Carrinho_empresa.objects.get(empresa=empresa)
                        carrinho.itemcarrinho_set.all().delete()

                        return redirect('/vetor5/faturas', fatura_id=fatura.id)
                    except Exception as e:
                        return HttpResponse(f"Erro ao criar a fatura: {e}", status=500)
                else:
                    return HttpResponse("O comprovativo é inválido.", status=400)

            except Exception as e:
                return HttpResponse(f"Erro interno do sistema: {e}", status=500)

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
    """
    Gera uma fatura para um pedido.
    """
    if 'gerente' in request.session:
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            cliente = pedido.usuario
            tipo_cliente = "Cliente"
            itens_pedido = pedido.item_pedido_set.all()
        except Pedido.DoesNotExist:
            pedido = get_object_or_404(Pedido_empresa, id=pedido_id)
            cliente = pedido.empresa
            tipo_cliente = "Empresa"
            itens_pedido = pedido.itempedidoempresa_set.all()

        valor_total = sum(item.quantidade * item.produto.preco for item in itens_pedido)
        imposto = valor_total * 0.10
        total_com_imposto = valor_total + imposto

        fatura = Fatura.objects.create(
            cliente=cliente if tipo_cliente == "Cliente" else None,
            empresa=cliente if tipo_cliente == "Empresa" else None,
            pedido=pedido,
            valor_total=valor_total
        )

        return render(request, 'pedido_empresa_gerente.html', {
            'fatura': fatura,
            'tipo_cliente': tipo_cliente,
            'pedido': pedido,
            'valor_total': valor_total,
            'imposto': imposto,
            'total_com_imposto': total_com_imposto,
            'cliente': cliente,
            'itens_pedido': itens_pedido
        })
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

from .models import ItemCarrinho, Carrinho, Carrinho_empresa
from django.http import HttpResponse 

def remover_produto_carrinho(request, produto_id):
    try:
        # Verifica se o cliente está logado 
        cliente_id = request.session.get('cliente')
        if cliente_id:
            cliente = get_object_or_404(Cliente, id=cliente_id)
            # A mudança principal:  Tenta obter o Carrinho usando filter
            carrinho = Carrinho.objects.filter(cliente=cliente).first() 

            if carrinho: 
                item = ItemCarrinho.objects.filter(produto_id=produto_id, carrinho=carrinho).first()  
                if item:  
                    item.delete()
                    return redirect('/vetor5/carrinho/')  
                else: 
                    return HttpResponse("Item não encontrado no carrinho.", status=404)
            else: 
                return HttpResponse("Você não tem itens em seu carrinho.", status=404)

        # Verifica se a empresa está logada 
        empresa_id = request.session.get('empresa')  
        if empresa_id:
            empresa = get_object_or_404(Empresas, id=empresa_id) 
            carrinho_empresa = Carrinho_empresa.objects.filter(empresa=empresa).first() # Obtem o carrinho com filter.
            if carrinho_empresa:
                item = ItemCarrinho.objects.filter(produto_id=produto_id, carrinho_empresa=carrinho_empresa).first() 
                if item:
                    item.delete()
                    return redirect('/vetor5/carrinho_empresa/') 
                else:
                    return HttpResponse("Item não encontrado no carrinho da empresa.", status=404)
            else:
                return HttpResponse("Você não tem itens no carrinho da empresa.", status=404)

        # Caso o usuário não esteja logado como empresa nem cliente 
        return HttpResponse("Você precisa estar logado para remover itens do carrinho.", status=403) 

    except (Cliente.DoesNotExist, Carrinho.DoesNotExist, Carrinho_empresa.DoesNotExist, ItemCarrinho.DoesNotExist):
        return HttpResponse("Carrinho ou Item não encontrado.", status=404)
    except Exception as e:
        return HttpResponse(f"Erro inesperado: {str(e)}", status=500)


def remover_produto_carrinho_empresa(request, produto_id):
    try:
        empresa_id = request.session.get('empresa')
        if not empresa_id:
            return redirect('/vetor5/login_empresa/?status=2')

        empresa = get_object_or_404(Empresas, id=empresa_id)
        carrinho_empresa = Carrinho_empresa.objects.filter(empresa=empresa).first()

        if carrinho_empresa: 
            item = get_object_or_404(ItemCarrinho, produto_id=produto_id, carrinho_empresa=carrinho_empresa)
            item.delete()
            return redirect('/vetor5/carrinho_empresa/')
        else:
            return HttpResponse("Carrinho da empresa está vazio.", status=404)

    except ItemCarrinho.DoesNotExist:
        return HttpResponse("Item não encontrado no carrinho.", status=404)
    except Carrinho_empresa.DoesNotExist:
        return HttpResponse("Carrinho não encontrado.", status=404)
    except Exception as e:
        return HttpResponse(f"Erro inesperado: {str(e)}", status=500)
    


'''
def adicionar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.cliente = request.user.cliente  
            endereco.save()
            return redirect('sucesso') 
    else:
        form = EnderecoForm()
    return render(request, 'endereco.html', {'form': form})
'''


def produtos_por_marca(request, marca_nome):
    # Filtra todas as instâncias da marca pelo nome
    marca = Marca_produto.objects.filter(nome=marca_nome)
    
    # Filtra os produtos que pertencem a qualquer uma das instâncias de marca encontradas
    produtos = Produtos.objects.filter(marca__in=marca)
    
    return render(request, 'nossas_marcas.html', {'produtos': produtos, 'marca': marca})

