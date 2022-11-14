from django.db import models
from django.contrib.auth.models import User


class Vendedor(models.Model):

    usuario = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    telefone = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.usuario.username

    @property
    def clientes(self):
        clientes =[pedido.cliente for pedido in self.pedido_set.filter(pagamento=True)]

        return clientes

    @property
    def count_endereco_cliente(self):
        uf_cont= {}
        for cliente in self.clientes:
            for endereco in cliente.endereco_set.all():
                if not endereco.uf in uf_cont:
                    print('NOT')
                    uf = {endereco.uf: 1}
                    uf_cont.update(uf)

                else:
                    print('ELSE')
                    uf = {endereco.uf: 1 + uf_cont[endereco.uf]}
                    uf_cont.update(uf)

        return uf_cont


