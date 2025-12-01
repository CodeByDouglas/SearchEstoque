import time
from django.shortcuts import render
from django.db import connection

from estoque import local_cache

def busca(request):
    resultado = None
    tempo_execucao = 0
    metodo = request.GET.get('metodo')
    termo = request.GET.get('termo')
    
    if termo and metodo:
        start_time = time.time()
        
        if metodo == 'indexada':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM estoque_produto WHERE nome = %s", [termo])
                row = cursor.fetchone()
                if row:
                    # Mapeando a tupla para um dicionário ou objeto simples
                    resultado = {
                        'id': row[0], 'nome': row[1], 'codigo': row[2], 
                        'quantidade': row[3], 'preco': row[4]
                    }

        elif metodo == 'sequencial':
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nome, codigo, quantidade, preco FROM estoque_produto")
                produtos = cursor.fetchall()
                
                for p in produtos:
                    if p[1] == termo: # Comparação de string
                        resultado = {
                            'id': p[0], 'nome': p[1], 'codigo': p[2], 
                            'quantidade': p[3], 'preco': p[4]
                        }
                        break

        elif metodo == 'hashmap':
            # Tenta pegar do cache local (variável global)
            mapa_produtos = local_cache.get_hashmap()
            
            if mapa_produtos is None:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id, nome, codigo, quantidade, preco FROM estoque_produto")
                    produtos = cursor.fetchall()
                    
                    # Construindo o HashMap (Dicionário)
                    mapa_produtos = {p[1]: p for p in produtos}
                    
                    # Salva no cache local
                    local_cache.set_hashmap(mapa_produtos)
            
            if termo in mapa_produtos:
                p = mapa_produtos[termo]
                resultado = {
                    'id': p[0], 'nome': p[1], 'codigo': p[2], 
                    'quantidade': p[3], 'preco': p[4]
                }

        end_time = time.time()
        tempo_execucao = (end_time - start_time) * 1000 # Convertendo para ms

    return render(request, 'estoque/busca.html', {
        'resultado': resultado,
        'tempo_execucao': f"{tempo_execucao:.4f}",
        'metodo': metodo,
        'termo': termo
    })
