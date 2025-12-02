from django.shortcuts import render, redirect
from django.db import connection

from estoque import local_cache

from django.db.models import Q
from estoque.models import Produto

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        codigo = request.POST.get('codigo')
        quantidade = request.POST.get('quantidade')
        preco = request.POST.get('preco')
        
        # Verifica se já existe produto com mesmo nome ou código
        if Produto.objects.filter(Q(nome=nome) | Q(codigo=codigo)).exists():
            return render(request, 'estoque/cadastro.html', {
                'error': 'Produto com este nome ou código já existe.',
                'nome': nome,
                'codigo': codigo,
                'quantidade': quantidade,
                'preco': preco
            })
        
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO estoque_produto (nome, codigo, quantidade, preco) VALUES (%s, %s, %s, %s)",
                [nome, codigo, quantidade, preco]
            )
            
        # Invalida o cache do HashMap para que o novo produto apareça na busca
        local_cache.invalidate_hashmap()
        
        return redirect('busca')
    return render(request, 'estoque/cadastro.html')
