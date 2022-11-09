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



def pedidos(request, cliente):

    clientes = Cliente.objects.filter(id=cliente)
    vendedor = Vendedor.objects.all()
    produtos = Juice.objects.all()
    pedidos = Pedido.objects.filter(cliente_id=cliente)
    item = Item.objects.all()
    context = {'clientes': clientes,
                'vendedor': vendedor,
                'produtos': produtos,
                'pedidos': pedidos,
                'item': item,
                }

    if request.method == "POST":

        cli = Cliente.objects.get(id=cliente)
        ven = Vendedor.objects.get(id=1)
        novo_pedido = Pedido(cliente= cli, vendedor=ven)

        novo_pedido.save()


    return render(request=request, template_name="pedidos.html",context= context)





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




