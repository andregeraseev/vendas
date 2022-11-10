from django.db import models
from clientes.models import Cliente
from vendedores.models import Vendedor
from produtos.models import Juice


class Item(models.Model):
    produto = models.ForeignKey(Juice, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def valor_total(self):
            return self.quantidade * 25



    def __str__(self):
        return str(self.produto.nome) + " " + str(self.produto.mg) + " " + str(self.quantidade) +"un"


class Pedido(models.Model):

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.BooleanField(default=False)
    pagamento = models.BooleanField(default=False)
    primeira_compra = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    @property
    def valor_total(self):
        quantidade= sum([int(item.quantidade) for item in self.items.all()])
        if quantidade >=20 and quantidade  <=49:
            return 22 * quantidade
        elif quantidade >=50 and quantidade  <=99:
            return 10 * quantidade
        elif quantidade >=100 and quantidade  <=199:
            return 18 * quantidade
        elif quantidade >= 200:
            return 17 * quantidade
        else:
            return quantidade * 25
        # return sum([item.valor_total for item in self.items.all()])

    @property
    def comicao(self):
        if self.primeira_compra == True:
            return  int(self.valor_total) * 0.10
        else:
            return int(self.valor_total) * 0.05



