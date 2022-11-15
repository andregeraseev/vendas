from django.db import models
from vendedores.models import Vendedor
from django.utils.text import slugify


class Cliente(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    nome = models.CharField(max_length=80)
    telefone = models.IntegerField(blank= True, null=True)
    email = models.EmailField(blank= True, null=True)
    cpf = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)



class Endereco(models.Model):
    UF = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'))



    cliente = models.ForeignKey(Cliente, on_delete= models.CASCADE)
    destinatario = models.CharField(max_length= 30, null=True, blank=True)
    apelido = models.CharField(max_length= 30, default= 'Endereço principal', blank=True)
    cep = models.IntegerField()
    logradouro = models.CharField(max_length=150)
    numero = models.IntegerField(max_length=5)
    bairro = models.CharField(max_length=30)
    uf = models.CharField(max_length = 2, choices=UF, null= True)
    complemento = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return self.cliente.nome + ' ' + self.apelido

    @property
    def destinatario_auto(self):
        if self.destinatario == None:
            return self.cliente.nome
        else:
            return self.destinatario





