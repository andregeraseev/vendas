from django.shortcuts import render, redirect
from .models import Endereco, Cliente
from .forms import EnderecoForm, ClienteForm
from vendedores.models import Vendedor
from django.contrib import messages
from pedidos.models import Pedido
from django.contrib.auth.decorators import login_required
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import urllib, base64
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable

@login_required
def clientes(request):
    clientes = Cliente.objects.filter(vendedor=request.user.vendedor.id)

    # inicio pandas vendas por estado
    cliente_df = Cliente.objects.filter(vendedor_id=request.user.vendedor.id).values('endereco__uf')

    df = pd.DataFrame(cliente_df).value_counts()

    fig, ax = plt.subplots()
    # ax = fig.add_axes([0, 0, 1, 1])
    ax.set_yticks(range(1, len(df)))
    make_axes_area_auto_adjustable(ax)

    df.plot( kind='bar', figsize=(13,5),title='Cliente por estado', x='endereco__uf', colormap='prism')
    plt.title("Clientes por estado")
    plt.xlabel('Estado')
    plt.xticks(rotation=0)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    # fim pandas

    # inicio pandas valor por cliente
    cliente_df_compra = Pedido.objects.filter(vendedor_id=request.user.vendedor.id, pagamento=True).values('cliente__nome','valor')


    df_valor = pd.DataFrame(cliente_df_compra)
    df_valor['valor'] = df_valor['valor'].astype(float)
    df_valor['cliente__nome'] = df_valor['cliente__nome'].astype(str)

    #
    print(df_valor)
    print(df_valor.dtypes)
    df_valor = df_valor.groupby('cliente__nome').sum()
    fig_valor, ax_valor = plt.subplots()
    # ax_valor = fig_valor.add_axes([0, 0, 1, 1])
    # ax_valor.set_yticks(range(1, len(df_valor)))
    make_axes_area_auto_adjustable(ax_valor)

    df_valor.plot(kind='bar', figsize=(13,7),title='Cliente por estado', colormap='prism')
    plt.xticks(rotation=0)
    plt.title("Valor de compra")
    plt.xlabel('cliente')

    buffer_valor = io.BytesIO()
    plt.savefig(buffer_valor, format='png')
    buffer_valor.seek(0)
    image_png_valor = buffer_valor.getvalue()
    buffer_valor.close()
    graphic_valor = base64.b64encode(image_png_valor)
    graphic_valor = graphic_valor.decode('utf-8')
    # fim pandas


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


    return render(request=request, template_name="clientes.html", context={ 'clientes': clientes,'graphic':graphic, 'graphic_valor': graphic_valor})
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

            vendedor_id =  request.user.vendedor.id
            # print(vendedor_id)
            vendedor =  Vendedor.objects.get(id=vendedor_id)
            # print(vendedor)
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
        # print(cliente)
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

