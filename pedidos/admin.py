from django.contrib import admin
from pedidos.models import Pedido, Item



class PedidoList(admin.ModelAdmin):
    list_display = ['id','valor_total']



admin.site.register(Pedido,PedidoList)




admin.site.register(Item)