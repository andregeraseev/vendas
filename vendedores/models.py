from django.db import models
from django.contrib.auth.models import User


class Vendedor(models.Model):

    usuario = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    telefone = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.usuario.username



