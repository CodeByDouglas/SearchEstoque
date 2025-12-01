from django.shortcuts import redirect
from django.db import connection

from estoque import local_cache

def atualizar_estoque(request, produto_id):
    if request.method == 'POST':
        acao = request.POST.get('acao')
        quantidade = int(request.POST.get('quantidade', 1))
        
        with connection.cursor() as cursor:
            if acao == 'adicionar':
                cursor.execute("UPDATE estoque_produto SET quantidade = quantidade + %s WHERE id = %s", [quantidade, produto_id])
            elif acao == 'subtrair':
                cursor.execute("UPDATE estoque_produto SET quantidade = quantidade - %s WHERE id = %s", [quantidade, produto_id])
        
        # Invalida o cache do HashMap para refletir a nova quantidade
        local_cache.invalidate_hashmap()
                
    return redirect(request.META.get('HTTP_REFERER', 'busca'))
