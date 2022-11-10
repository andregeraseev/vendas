from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from clientes.models import Cliente
from pedidos.models import Pedido

def dashboard(request):
    clientes = Cliente.objects.filter(vendedor=request.user.id)
    pedidos = Pedido.objects.filter(vendedor=request.user.id)
    context = {
        'pedidos': pedidos,
        'clientes': clientes}


    return render(request=request, template_name="dashboard.html",context = context)


def login(request):
    """Realiza o login de uma pessoa no sistema"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.warning(request, 'Os campos email e senha não podem ficar em branco')
            return redirect('dashboard')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)

            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
                return redirect('dashboard')
            # erro senha errada
            else:
                messages.warning(request, 'Verifique sua senha')
                return redirect('login')

        else:
            messages.warning(request, 'Seu email ou sua senha estão incorretos')
            return redirect('login')
    return render(request=request, template_name="login.html")


def logout(request):
    auth.logout(request)
    return redirect('login')
# Create your views here.


def campo_vazio(campo):
    return not campo.strip()


def senhas_nao_sao_iguais(senha, senha2):
    return senha != senha2