"""setup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from clientes.views import cadastro_com_endereco,cadastro_sem_endereco,cadastro_endereco,clientes
from pedidos.views import pedido,pedidos,tirar_item,adicionar_item,mudar_status,imprimir,todos_pedidos
from vendedores.views import login,logout,dashboard

urlpatterns = [

    path('admin/', admin.site.urls),
    path('clientes', clientes, name='clientes'),
    path('pedidos', todos_pedidos, name='pedidos'),
    path('dashboard', dashboard, name='dashboard'),
    path('', dashboard, name='dashboard'),
    path('cadastro_com_endereco', cadastro_com_endereco, name='cadastro_com_endereco'),
    path('cadastro_sem_endereco', cadastro_sem_endereco, name='cadastro_sem_endereco'),
    path('cadastro_endereco/<int:id>', cadastro_endereco, name='cadastro_endereco'),
    path('pedidos/<slug:cliente>', pedidos, name='pedidos'),
    path('pedido/<slug:cliente>/<int:pedido>/', pedido, name='pedido'),
    path('pedido/<slug:cliente>/<int:pedido>/tirar_item', tirar_item, name='tirar_item'),
    path('pedido/<slug:cliente>/<int:pedido>/adicionar_item', adicionar_item, name='adicionar_item'),
    path('pedido/<slug:cliente>/<int:pedido>/mudar_status', mudar_status, name='mudar_status'),
    path('pedido/<slug:cliente>/<int:pedido>/imprimir', imprimir, name='imprimir'),
    path('accounts/login', login, name='login'),
    path('logout', logout, name='logout'),

]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)