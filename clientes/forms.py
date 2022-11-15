from django import forms

from .models import Endereco, Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nome', 'telefone', 'email', 'cpf',)



class EnderecoForm(forms.ModelForm):
     class Meta:
        model = Endereco
        fields = ('destinatario','apelido','cep','logradouro','numero','bairro','uf','complemento')
        # widgets = {'cliente': forms.HiddenInput()}
