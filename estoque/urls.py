from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('busca/', views.busca, name='busca'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('atualizar/<int:produto_id>/', views.atualizar_estoque, name='atualizar_estoque'),
]
