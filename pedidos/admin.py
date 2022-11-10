from django.contrib import admin
from pedidos.models import Pedido, Item



class PedidoList(admin.ModelAdmin):
    list_display = ['id','cliente','vendedor','valor_total','status','primeira_compra','pagamento']
    list_editable = ('vendedor','status','primeira_compra','pagamento',)
    ordering = ('-created_at',)
    list_filter = ('cliente', 'vendedor', 'status','primeira_compra','pagamento',)
    list_per_page = 30



admin.site.register(Pedido,PedidoList)




admin.site.register(Item)