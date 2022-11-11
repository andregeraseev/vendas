from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from clientes.models import Cliente
from pedidos.models import Pedido,Item
import datetime

def dashboard(request):
    hoje = datetime.date.today()
    mes_atual = hoje.strftime('%m')

    clientes = Cliente.objects.filter(vendedor=request.user.id)
    pedidos = Pedido.objects.filter(vendedor=request.user.id)
    pedidos_pagos = Pedido.objects.filter(pagamento=True, vendedor=request.user.id, created_at__gte=datetime.date(2022,int(mes_atual),1), created_at__lte=datetime.date(2022,int(mes_atual),30))
    pedidos_comicao_nao_paga = Pedido.objects.filter(pagamento=True, vendedor=request.user.id, recebido=False)
    comicao_pendente = sum([pedido.comicao for pedido in pedidos_comicao_nao_paga])
    items = Item.objects.filter(pedido__vendedor=request.user.id, pedido__pagamento=True)
    # item_pedido = {item.produto : item.quantidade for item in items}

    item_p = {}
    for item in items:
        item_novo ={item.produto: item.quantidade}
        if item.produto in item_p:
            print("existe", item.produto)
            item_novo= {item.produto : item.quantidade + item_p[item.produto]}
            item_p.update(item_novo)
        else:
            item_p.update(item_novo)


    print(item_p)

    venda=  sum([pedido.valor_total for pedido in pedidos_pagos])


    context = {
        'item_p': item_p,
        'comicao_pendente':comicao_pendente,
        'venda':venda,
        'pedidos_pagos': pedidos_pagos,
        'pedidos': pedidos,
        'clientes': clientes}




    return render(request=request, template_name="dashboard.html",context = context)


def login(request):
    """Realiza o login de uma pessoa no sistema"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.warning(request, 'Os campos email e senha não podem ficar em branco')
            return redirect('dashboard')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)

            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
                return redirect('dashboard')
            # erro senha errada
            else:
                messages.warning(request, 'Verifique sua senha')
                return redirect('login')

        else:
            messages.warning(request, 'Seu email ou sua senha estão incorretos')
            return redirect('login')
    return render(request=request, template_name="login.html")


def logout(request):
    auth.logout(request)
    return redirect('login')
# Create your views here.


def campo_vazio(campo):
    return not campo.strip()


def senhas_nao_sao_iguais(senha, senha2):
    return senha != senha2