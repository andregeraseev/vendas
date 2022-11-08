from django.db import models


class Juice(models.Model):
    NIC = (
        ("0mg", "0"),
        ("3mg", "3"),
        ("6mg", "6"),
        ("9mg", "9"),
        ("12mg", "12"),
    )

    nome = models.CharField(max_length=50)
    mls = models.IntegerField()
    mg = models.CharField(max_length= 4, choices = NIC,
        default ='0')
    valor = models.DecimalField(max_digits=8,decimal_places=2)
    descricao = models.TextField(max_length=800)
    criado = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    imagem = models.ImageField(upload_to='static/juices', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.nome + " " + str(self.mls) + "mls " + str(self.mg)








