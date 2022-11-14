from django.http import HttpResponse
from django.shortcuts import render,redirect
from clientes.models import Cliente
from vendedores.models import Vendedor
from produtos.models import Juice
from pedidos.models import Pedido,Item
from django.contrib import messages
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
import datetime





@login_required
def todos_pedidos(request):
    hoje = datetime.date.today()
    mes_atual = hoje.strftime('%m')
    vendedor = Vendedor.objects.filter(id=request.user.vendedor.id)
    clientes = Cliente.objects.filter(vendedor=request.user.vendedor.id)
    pedidos = Pedido.objects.filter(vendedor=request.user.vendedor.id)
    pedidos_pagos = Pedido.objects.filter(pagamento=True, vendedor=request.user.vendedor.id,
                                          created_at__gte=datetime.date(2022, int(mes_atual), 1),
                                          created_at__lte=datetime.date(2022, int(mes_atual), 30))
    pedidos_comicao_nao_paga = Pedido.objects.filter(pagamento=True, vendedor=request.user.vendedor.id, recebido=False)
    comicao_pendente = sum([pedido.comicao for pedido in pedidos_comicao_nao_paga])
    items = Item.objects.filter(pedido__vendedor=request.user.vendedor.id, pedido__pagamento=True)
    # item_pedido = {item.produto : item.quantidade for item in items}

    item_p = {}
    for item in items:
        item_novo = {item.produto: item.quantidade}
        if item.produto in item_p:
            print("existe", item.produto)
            item_novo = {item.produto: item.quantidade + item_p[item.produto]}
            item_p.update(item_novo)
        else:
            item_p.update(item_novo)

    uf_cont = {}

    for cliente in clientes:
        for endereco in cliente.endereco_set.all():
            if not endereco.uf in uf_cont:

                uf = {endereco.uf: 1}
                uf_cont.update(uf)

            else:

                uf = {endereco.uf: 1 + uf_cont[endereco.uf]}
                uf_cont.update(uf)
    print(uf_cont, item_p)


    venda = sum([pedido.valor_total for pedido in pedidos_pagos])

    context = {
        'uf_cont':uf_cont,
        'vendedor' : vendedor,
        'item_p': item_p,
        'comicao_pendente': comicao_pendente,
        'venda': venda,
        'pedidos_pagos': pedidos_pagos,
        'pedidos': pedidos,
        'clientes': clientes}

    return render(request=request, template_name="todos_pedidos.html", context=context)





@login_required
def pedidos(request, cliente):

    clientes = Cliente.objects.filter(id=cliente)
    vendedor = Vendedor.objects.all()
    produtos = Juice.objects.all()
    pedidos = Pedido.objects.filter(cliente_id=cliente)
    item = Item.objects.all()
    items_mais_vendidos = Item.objects.filter(pedido__vendedor=request.user.vendedor.id, pedido__pagamento=True,pedido__cliente__id=cliente)

    item_p = {}
    for item in items_mais_vendidos:
        item_novo = {item.produto: item.quantidade}
        if item.produto in item_p:
            print("existe", item.produto)
            item_novo = {item.produto: item.quantidade + item_p[item.produto]}
            item_p.update(item_novo)
        else:
            item_p.update(item_novo)


    context = {

        'item_p':item_p,
        'clientes': clientes,
                'vendedor': vendedor,
                'produtos': produtos,
                'pedidos': pedidos,
                'item': item,
                }

    if request.method == "POST":
        vendedor_id = request.user.vendedor.id
        cli = Cliente.objects.get(id=cliente)
        ven = Vendedor.objects.get(id=vendedor_id)
        if not pedidos:
            print("PRimeiRO Pedido")
            novo_pedido = Pedido(cliente=cli, vendedor=ven, primeira_compra=True)
            novo_pedido.save()
            return redirect(f"/pedido/{cli.slug}/{novo_pedido.id}")
        else:
            print("JA TEM PEDIDOS")
            novo_pedido = Pedido(cliente= cli, vendedor=ven)
            novo_pedido.save()
            return redirect(f"/pedido/{cli.slug}/{novo_pedido.id}")

        return render(request=request, template_name="pedidos.html", context=context)

    return render(request=request, template_name="pedidos.html",context= context)




@login_required
def pedido(request,cliente,pedido):
    clientes = Cliente.objects.filter(slug=cliente)
    vendedor = Vendedor.objects.all()
    produtos0mg = Juice.objects.filter(mg="0mg").order_by('nome')
    produtos3mg = Juice.objects.filter(mg="3mg").order_by('nome')
    produtos6mg = Juice.objects.filter(mg="6mg").order_by('nome')
    produtos9mg = Juice.objects.filter(mg="9mg").order_by('nome')
    produtos12mg = Juice.objects.filter(mg="12mg").order_by('nome')
    pedidos = Pedido.objects.filter(pk=pedido)
    item = Item.objects.all()
    context = {'cliente': clientes,
               'vendedor': vendedor,
               'produtos0mg': produtos0mg,
               'produtos3mg': produtos3mg,
               'produtos6mg': produtos6mg,
               'produtos9mg': produtos9mg,
               'produtos12mg': produtos12mg,
               'pedidos': pedidos,
               'item': item,
               }

    # if request.method == 'POST' and 'id_produto' in request.POST: #ADICONAR PRODUTO
    #     try:
    #         order = Pedido.objects.get(id=pedido, status= False)
    #
    #         quantidade = request.POST["quantidade"]
    #         id_produto = request.POST["id_produto"]
    #
    #         if int(quantidade) <= 0:
    #             messages.warning(request, 'A quantidade de items tem que ser maior que 0')
    #         else:
    #
    #             produto = Juice.objects.get(pk=id_produto)
    #             item = Item(produto=produto,
    #                         quantidade=quantidade,
    #                         )
    #             item.save()
    #
    #             order.items.add(item)
    #
    #     except:
    #         messages.error(request, 'Este pedido esta fechado, voce nao pode adicionar items', 'danger')

    # if request.method == 'POST' and 'remover_id' in request.POST:  # REMOVER PRODUTO
    #     try:
    #         order = Pedido.objects.get(id=pedido, status=False)
    #         remover = request.POST["remover_id"]
    #
    #         order.items.remove(remover)
    #
    #     except:
    #         messages.error(request, 'Este pedido esta fechado, voce nao pode remover items', 'danger')


    # if request.method == 'POST' and 'mudar_status' in request.POST:
    #
    #     order = Pedido.objects.filter(id=pedido)
    #     if order.filter(status=False):
    #         order.update(
    #             status=True)
    #         messages.error(request, 'Pedido Fechado', 'danger')
    #     else:
    #         order.update(
    #             status=False)
    #         messages.error(request, 'Pedido Aberto', 'success')

    return render(request=request, template_name="pedido.html",context=context)



@login_required
def imprimir(request,cliente,pedido):
    clientes = Cliente.objects.filter(slug=cliente)
    vendedor = Vendedor.objects.all()
    produtos0mg = Pedido.objects.filter(id=pedido,items__produto__mg="0mg")
    produtos3mg = Juice.objects.filter(mg="3mg").order_by('nome')
    produtos6mg = Juice.objects.filter(mg="6mg").order_by('nome')
    produtos9mg = Juice.objects.filter(mg="9mg").order_by('nome')
    produtos12mg = Juice.objects.filter(mg="12mg").order_by('nome')
    pedidos = Pedido.objects.get(pk=pedido)
    item0mg = pedidos.items.filter(produto__mg='0mg').order_by('produto')
    item3mg = pedidos.items.filter(produto__mg='3mg').order_by('produto')
    item6mg  = pedidos.items.filter(produto__mg='6mg ').order_by('produto')
    item9mg = pedidos.items.filter(produto__mg='6mg').order_by('produto')
    item12mg = pedidos.items.filter(produto__mg='12mg').order_by('produto')

    context = {'clientes': clientes,
               'vendedor': vendedor,
               'produtos0mg': produtos0mg,
               'produtos3mg': produtos3mg,
               'produtos6mg': produtos6mg,
               'produtos9mg': produtos9mg,
               'produtos12mg': produtos12mg,
               'item0mg':item0mg,
               'item3mg':item3mg,
               'item6mg':item6mg,
               'item9mg':item9mg,
               'item12mg':item12mg,
               'pedidos': pedidos,

               }


    return render(request=request, template_name="imprimir.html",context=context)

@login_required
def mudar_status(request,cliente,pedido):

    if request.method == "POST":

        order = Pedido.objects.get(id=pedido)
        print(order.status)

        if order.status == False:
            orders = Pedido.objects.filter(id=pedido)
            orders.update(status=True)
            data = {'status': 'success','ativo': "ABRIR PEDIDO"}
            return JsonResponse(data, status=200)

        elif order.status == True:
            orders = Pedido.objects.filter(id=pedido)
            orders.update(status=False)
            data = {'status': 'success', 'ativo':"FECHAR PEDIDO" }
            print( order.status)
            return JsonResponse(data, status=200)

        else:
            data = {'status': 'error'}
            return JsonResponse(data, status=400)


    # if request.method == 'POST':
    #     startsession = Pedido.objects.get(id=pedido)
    #     startsession.status = True if request.POST.get('ativo') == 'true' else False
    #     startsession.save()
    #     data = {'status': 'success', 'ativo': startsession.status}
    #     return JsonResponse(data, status=200)
    # else:
    #     data = {'status': 'error'}
    #     return JsonResponse(data, status=400)


# def mudar_status(request,cliente,pedido):
#     if request.method == 'POST' and 'mudar_status' in request.POST:
#
#         order = Pedido.objects.filter(id=pedido)
#         if order.filter(status=False):
#             order.update(
#                 status=True)
#             messages.error(request, 'Pedido Fechado', 'danger')
#         else:
#             order.update(
#                 status=False)
#             messages.error(request, 'Pedido Aberto', 'success')
#     return redirect(f"/pedido/{cliente}/{pedido}")
@login_required
def tirar_item(request,cliente,pedido):
    if request.method == 'POST':  # REMOVER PRODUTO
        try:
            order = Pedido.objects.get(id=pedido, status=False)
            remover = request.POST["remover_id"]

            order.items.remove(remover)
            messages.success(request, 'Item removido')
            return  redirect(f"/pedido/{cliente}/{pedido}")

        except:
            messages.error(request, 'Este pedido esta fechado, voce nao pode remover items', 'danger')
            return  redirect(f"/pedido/{cliente}/{pedido}")

@login_required
def adicionar_item(request,cliente,pedido):
    # pedidos = serializers.serialize('json',Pedido.objects.filter(pk=pedido))
    pedidos = Pedido.objects.filter(pk=pedido)
    if request.method == 'POST':  # ADICONAR PRODUTO
        try:
            order = Pedido.objects.get(id=pedido, status=False)

            quantidade = request.POST["quantidade"]
            id_produto = request.POST["id_produto"]
            print(quantidade, id_produto)
            if int(quantidade) <= 0:
                data = { "pedidos": pedidos}
                messages.error(request, '"quantidade inferior a 1"', 'danger')
                return render(request, 'partials/_items.html',  data)
            else:

                produto = Juice.objects.get(pk=id_produto)
                item = Item(produto=produto,
                            quantidade=quantidade,
                            )
                item.save()

                order.items.add(item)
                data = {"pedidos": pedidos}

                messages.success(request, 'Item adicionado', 'success')

                return render(request, 'partials/_items.html',  data)

        except:
            data = {"pedidos": pedidos}
            messages.error(request, 'pedido fechado', 'success')
            return render(request, 'partials/_items.html',  data)









#
# def adicionar_item(request,cliente,pedido):
#     if request.method == 'POST' and 'id_produto' in request.POST:  # ADICONAR PRODUTO
#         try:
#             order = Pedido.objects.get(id=pedido, status=False)
#
#             quantidade = request.POST["quantidade"]
#             id_produto = request.POST["id_produto"]
#
#             if int(quantidade) <= 0:
#                 messages.warning(request, 'A quantidade de items tem que ser maior que 0')
#             else:
#
#                 produto = Juice.objects.get(pk=id_produto)
#                 item = Item(produto=produto,
#                             quantidade=quantidade,
#                             )
#                 item.save()
#
#                 order.items.add(item)
#
#         except:
#             messages.error(request, 'Este pedido esta fechado, voce nao pode adicionar items', 'danger')
#
#     return redirect(f"/pedido/{cliente}/{pedido}")
# def mudar_status(request):




