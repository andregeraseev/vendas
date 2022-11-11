from django.shortcuts import render, redirect
from .models import Endereco, Cliente
from .forms import EnderecoForm, ClienteForm
from vendedores.models import Vendedor
from django.contrib import messages
from pedidos.models import Pedido,Item
from django.contrib.auth.decorators import login_required

@login_required
def clientes(request):
    clientes = Cliente.objects.filter(vendedor=request.user.id)


    # if request.method == "POST":#adiciona pedido para cliente
    #
    #     cliente = request.POST['cliente_id']
    #     print(cliente)
    #     vendedor_id = request.user.id
    #     cli = Cliente.objects.get(id=cliente)
    #     ven = Vendedor.objects.get(id=vendedor_id)
    #     pedidos = Pedido.objects.filter(cliente_id=cliente)
    #     if not pedidos:
    #         print("PRimeiRO Pedido")
    #         novo_pedido = Pedido(cliente=cli, vendedor=ven, primeira_compra=True)
    #         novo_pedido.save()
    #         return redirect(f"/pedido/{cli.slug}/{novo_pedido.id}")
    #     else:
    #         print("JA TEM PEDIDOS")
    #         novo_pedido = Pedido(cliente=cli, vendedor=ven)
    #         novo_pedido.save()
    #         return redirect(f"/pedido/{cli.slug}/{novo_pedido.id}")
    #     return redirect(f"/pedido/{cli.slug}/{novo_pedido.id}")


    return render(request=request, template_name="clientes.html", context={ 'clientes': clientes})
@login_required
def cadastro_sem_endereco(request):
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid():
            cliente_form.save()
            messages.success(request, ('O endereço foi salvo!'))
        else:
            messages.error(request, 'Error salvar o formulario')
            return redirect("cadastro_sem_endereco")
    cliente_form = ClienteForm()

    return render(request=request, template_name="cadastro_sem_endereco.html",
                  context={ 'cliente_form': cliente_form})

@login_required
def cadastro_com_endereco(request):
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        endereco_form = EnderecoForm(request.POST)

        if endereco_form.is_valid() and cliente_form.is_valid():

            vendedor_id =  request.user.id
            vendedor =  Vendedor.objects.get(id=vendedor_id)
            print(vendedor)
            nome = cliente_form.cleaned_data['nome']
            telefone = cliente_form.cleaned_data['telefone']
            email = cliente_form.cleaned_data['email']
            cpf = cliente_form.cleaned_data['cpf']

            apelido = endereco_form.cleaned_data['apelido']
            cep = endereco_form.cleaned_data['cep']
            logradouro = endereco_form.cleaned_data['logradouro']
            numero = endereco_form.cleaned_data['numero']
            bairro = endereco_form.cleaned_data['bairro']
            uf = endereco_form.cleaned_data['uf']

            cliente = Cliente.objects.create(
                vendedor=vendedor,
                nome=nome,
                telefone=telefone,
                email=email,
                cpf=cpf,

            )

            # cliente = cliente.save(commit=False)


            form = Endereco(cliente=cliente,
                     apelido=apelido,
                     cep=cep,
                     logradouro=logradouro,
                     numero=numero,
                     bairro=bairro,
                     uf=uf,
                     complemento = "teste 123"
                            )



            cliente.save()
            form.save()
            messages.success(request, ('O endereço foi salvo!'))
            return redirect("dashboard")
        else:
            messages.error(request, 'Error salvar o formulario')

        return redirect("cadastro_com_endereco")
    endereco_form = EnderecoForm()
    cliente_form = ClienteForm()
    endereco = Endereco.objects.all()
    return render(request=request, template_name="cadastro_com_endereco.html", context={'endereco_form': endereco_form, 'endereco': endereco, 'cliente_form':cliente_form})

@login_required
def cadastro_endereco(request, id):
    if request.method == "POST":
        cliente = Cliente.objects.get(id=id)
        print(cliente)
        endereco_form = EnderecoForm(request.POST)

        if endereco_form.is_valid():

            # cliente = endereco_form.cleaned_data['cliente']
            apelido = endereco_form.cleaned_data['apelido']
            cep = endereco_form.cleaned_data['cep']
            logradouro = endereco_form.cleaned_data['logradouro']
            numero = endereco_form.cleaned_data['numero']
            bairro = endereco_form.cleaned_data['bairro']
            uf = endereco_form.cleaned_data['uf']



            form = Endereco(cliente=cliente,
                     apelido=apelido,
                     cep=cep,
                     logradouro=logradouro,
                     numero=numero,
                     bairro=bairro,
                     uf=uf,
                     complemento = "teste 123"
                            )


            form.save()
            messages.success(request, ('O endereço foi salvo!'))
        else:
            messages.error(request, 'Error salvar o formulario')

        return redirect("clientes")
    endereco_form = EnderecoForm()
    endereco = Endereco.objects.all()
    return render(request=request, template_name="cadastro_endereco.html", context={'endereco_form': endereco_form, 'endereco': endereco})

