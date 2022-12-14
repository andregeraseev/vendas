from django.http import HttpResponse
from django.shortcuts import render,redirect
from clientes.models import Cliente,Endereco
from vendedores.models import Vendedor
from produtos.models import Juice
from pedidos.models import Pedido,Item
from django.contrib import messages
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import urllib, base64
from django.utils import timezone
import calendar
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable
import numpy as np



@login_required
def todos_pedidos(request):
    hoje = datetime.datetime.now(tz=timezone.utc)
    if request.method == "POST":
        data_inicio = request.POST["data_inicio"]
        data_fim = request.POST["data_fim"]

        ano_atual = int(data_inicio[6:10])
        mes_atual = int(data_inicio[3:5])
        incio_dia = int(data_inicio[0:2])
        proximo_ano = int(data_fim[6:10])
        proximo_mes = int(data_fim[3:5])
        fim_dia = int(data_fim[0:2])
        dias_no_mes = datetime.datetime(proximo_ano, proximo_mes, fim_dia) - datetime.datetime(ano_atual, mes_atual,
                                                                                               incio_dia)

        if dias_no_mes.days <= 0:

            incio_dia = 1
            mes_atual = int(hoje.strftime('%m'))
            ano_atual = int(hoje.strftime('%Y'))
            proximo_mes = int(mes_atual) + 1 if mes_atual != 12 else 1
            proximo_ano = ano_atual if mes_atual != 12 else int(ano_atual) + 1
            fim_dia = 1
            _, dias_no_mes = calendar.monthrange(int(ano_atual), int(mes_atual))
            data = pd.date_range(f'{mes_atual}/1/{ano_atual}', periods=dias_no_mes)
            messages.error(request,'Data de inicio não pode ser menor que data final', 'danger')


        else:

            ano_atual = int(data_inicio[6:10])
            mes_atual= int(data_inicio[3:5])
            incio_dia = int(data_inicio[0:2])
            proximo_ano = int(data_fim[6:10])
            proximo_mes = int(data_fim[3:5])
            fim_dia = int(data_fim[0:2])
            dias_no_mes = datetime.datetime(proximo_ano,proximo_mes, fim_dia) - datetime.datetime(ano_atual,mes_atual,incio_dia)

            data = pd.date_range(f'{mes_atual}/{incio_dia}/{ano_atual}', periods=dias_no_mes.days)



    else:
        incio_dia = 1
        mes_atual = int(hoje.strftime('%m'))
        ano_atual = int(hoje.strftime('%Y'))
        proximo_mes = int(mes_atual) + 1 if mes_atual != 12 else 1
        proximo_ano = ano_atual if mes_atual != 12 else int(ano_atual) + 1
        fim_dia =1
        _, dias_no_mes = calendar.monthrange(int(ano_atual), int(mes_atual))
        data = pd.date_range(f'{mes_atual}/1/{ano_atual}', periods=dias_no_mes)
    # inicio pandas


    item = Pedido.objects.filter(pagamento=True, status=True,
                                 data__gte=datetime.date(int(ano_atual), int(mes_atual), int(incio_dia)),
                                 data__lte=datetime.date(int(proximo_ano), int(proximo_mes), int(fim_dia)),
                                 vendedor_id=request.user.vendedor.id).values('data','valor')

    if len(item) >= 1:
        df = pd.DataFrame(item)
    else:
        item = [{'data': datetime.datetime(ano_atual, mes_atual, 1, tzinfo=datetime.timezone.utc), 'valor': float('0.00')}]
        df = pd.DataFrame(item)
    df['data'] = pd.to_datetime(df['data'],format='%Y-%m-%d').dt.strftime('%Y-%m-%d') #format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
    df['valor'] = df['valor'].astype(float)

    new_df = pd.DataFrame({'data': data})
    new_df['data'] = pd.to_datetime(new_df['data'],format='%Y-%m-%d').dt.strftime('%Y-%m-%d') #format='%d-%m-%Y').dt.strftime('%d-%m-%Y')

    m = pd.merge(df, new_df, how='outer')
    m= m.groupby('data').sum()
    m.fillna(0,inplace=True)

    fig, ax = plt.subplots()
    ax.set_xticks(range( 0, len(m)))
    make_axes_area_auto_adjustable(ax)

    m.plot(figsize=(13,5), colormap='prism', grid=True, ax=ax)
    plt.xticks(rotation=90)


    plt.title("Vendas do mes")
    plt.xlabel('data')
    plt.ylabel("valor");
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    #fim pandas


    vendedor = Vendedor.objects.filter(id=request.user.vendedor.id)
    clientes = Cliente.objects.filter(vendedor=request.user.vendedor.id)
    pedidos = Pedido.objects.filter(vendedor=request.user.vendedor.id)
    pedidos_pagos_uf = Pedido.objects.filter(pagamento=True, vendedor=request.user.vendedor.id)
    pedidos_pagos = Pedido.objects.filter(pagamento=True, vendedor=request.user.vendedor.id,
                                          data__gte=datetime.date(int(ano_atual), int(mes_atual), int(incio_dia)),
                                          data__lte=datetime.date(int(ano_atual), int(proximo_mes), int(fim_dia))).order_by('id')
    pedidos_comicao_nao_paga = Pedido.objects.filter(pagamento=True, vendedor=request.user.vendedor.id, recebido=False)
    comicao_pendente = sum([pedido.comicao for pedido in pedidos_comicao_nao_paga])
    items = Item.objects.filter(pedido__vendedor=request.user.vendedor.id, pedido__pagamento=True)
    # item_pedido = {item.produto : item.quantidade for item in items}

    item_p = {}
    for item in items:
        item_novo = {item.produto: item.quantidade}
        if item.produto in item_p:
            # print("existe", item.produto)
            item_novo = {item.produto: item.quantidade + item_p[item.produto]}
            item_p.update(item_novo)
        else:
            item_p.update(item_novo)

    uf_cont = {}

    for pedido in pedidos_pagos_uf:

            if not pedido.endereco.uf in uf_cont:

                uf = {pedido.endereco.uf: 1}
                uf_cont.update(uf)

            else:

                uf = {pedido.endereco.uf: 1 + uf_cont[pedido.endereco.uf]}
                uf_cont.update(uf)
    # print(uf_cont, item_p)


    venda = sum([pedido.valor_total for pedido in pedidos_pagos])

    context = {
        'graphic':graphic,
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
    enderecos = Endereco.objects.filter(cliente__slug=cliente)
    endereco_ativo = Endereco.objects.filter(ativo= True, cliente__slug=cliente)
    # produtos3mg = Juice.objects.filter(mg="3mg").order_by('nome')
    # produtos6mg = Juice.objects.filter(mg="6mg").order_by('nome')
    # produtos9mg = Juice.objects.filter(mg="9mg").order_by('nome')
    # produtos12mg = Juice.objects.filter(mg="12mg").order_by('nome')
    pedidos = Pedido.objects.filter(pk=pedido)
    item = Item.objects.all()
    context = {'cliente': clientes,
               'vendedor': vendedor,
               'produtos0mg': produtos0mg,
               'enderecos':enderecos,
               'endereco_ativo':endereco_ativo,
               # 'produtos3mg': produtos3mg,
               # 'produtos6mg': produtos6mg,
               # 'produtos9mg': produtos9mg,
               # 'produtos12mg': produtos12mg,
               'pedidos': pedidos,
               'item': item,
               }

    if request.method == 'POST' and 'id_produto' in request.POST: #ADICONAR PRODUTO

        try:
            order = Pedido.objects.get(id=pedido, status= False)

            quantidade = request.POST["quantidade"]
            id_produto = request.POST["id_produto"]
            mg = request.POST.get('mg', False)
            # tresmg = request.POST.get('tresmg', False)
            # seismg = request.POST.get('seismg', False)
            # novemg = request.POST.get('novemg', False)
            # dozemg = request.POST.get('dozemg', False)
            print
            if mg:
                print(mg)
            else:
                messages.warning(request, 'Escolha o mg')
                return render(request=request, template_name="tirar_pedido.html", context=context)

            print(order)
            if int(quantidade) <= 0:
                messages.warning(request, 'A quantidade de items tem que ser maior que 0')
            else:

                produto = Juice.objects.get(nome=id_produto, mg=mg)

                if Item.objects.filter(pedido=order, produto__nome= id_produto, produto__mg=mg):

                    item_update = Item.objects.filter(pedido=order, produto__nome=id_produto, produto__mg=mg)
                    quantidade_update = int(Item.objects.get(pedido=order,
                                                             produto__nome=id_produto,
                                                             produto__mg=mg).quantidade) + int(quantidade)
                    item_update.update(quantidade=quantidade_update)

                else:

                    item = Item(produto=produto,
                                quantidade=quantidade,
                                )
                    item.save()

                    order.items.add(item)

        except:
            messages.error(request, 'Este pedido esta fechado, voce nao pode adicionar items', 'danger')

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

    return render(request=request, template_name="tirar_pedido.html",context=context)



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
    item6mg  = pedidos.items.filter(produto__mg='6mg').order_by('produto')
    item9mg = pedidos.items.filter(produto__mg='9mg').order_by('produto')
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



        if not order.endereco:
            print(order.endereco)
            try:
                endereco_ativo = Endereco.objects.get(cliente__slug= cliente, ativo= True)
                Pedido.objects.filter(id=pedido).update(endereco=endereco_ativo)
                orders = Pedido.objects.filter(id=pedido)
                valor_total = order.valor_total
                Pedido.objects.filter(id=pedido).update(valor=valor_total)
                orders.update(status=True)
                data = {'status': 'success', 'ativo': "ABRIR PEDIDO", }
                return JsonResponse(data, status=200)
            except:
                data = {'status': 'success', 'pedidofechado': 'escolha um endereco teste', 'ativo': "FECHAR PEDIDO"}
                return JsonResponse(data, status=200)


        elif order.status == False:#caso o pedido esteja aberto fecha o pedido e da o valor total

            orders = Pedido.objects.filter(id=pedido)
            valor_total = order.valor_total
            Pedido.objects.filter(id=pedido).update(valor=valor_total)
            orders.update(status=True)
            data = {'status': 'success','ativo': "ABRIR PEDIDO",}
            return JsonResponse(data, status=200)

        elif order.status == True:

            orders = Pedido.objects.filter(id=pedido)
            Pedido.objects.filter(id=pedido).update(valor=None)
            orders.update(status=False)
            data = {'status': 'success', 'ativo':"FECHAR PEDIDO" }

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

        try:# caso o pedido esteja aberto
            order = Pedido.objects.get(id=pedido, status=False)

            quantidade = request.POST["quantidade"]
            id_produto = request.POST["id_produto"]

            if int(quantidade) <= 0:# verifica se a quantidade eh maior que um
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

        except:# caso o pedido esteja fechado nao deixa modificar
            data = {"pedidos": pedidos}
            messages.error(request, 'pedido fechado', 'danger')
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




def escolher_endereco(request,cliente,pedido):
    if request.method == 'POST':  # Seleciona endereco

            Endereco.objects.filter(cliente__slug=cliente).update(ativo=False)#deixa todos endereços do cliente como ativo = False
            endereco_ativo = request.POST["endereco_ativo"]
            Endereco.objects.filter(id=endereco_ativo).update(ativo=True)# endereço atual fica como Ativo

            Pedido.objects.filter(id=pedido).update(endereco=endereco_ativo)# adiciona esse endereço ao pedido

    return redirect(f"/pedido/{cliente}/{pedido}")


def desconto(request,cliente,pedido):
    if request.method == 'POST':  # Seleciona endereco

        desconto = request.POST['desconto']
        Pedido.objects.filter(id=pedido).update(desconto=desconto)



    return redirect(f"/pedido/{cliente}/{pedido}")