import random
from django.core.management.base import BaseCommand
from faker import Faker
from estoque.models import Produto

class Command(BaseCommand):
    help = 'Popula o banco de dados com produtos reais em português'

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')
        self.stdout.write('Iniciando população do banco com dados reais...')

        produtos_base = [
            'Arroz', 'Feijão', 'Macarrão', 'Açúcar', 'Sal', 'Café', 'Leite', 'Farinha de Trigo', 
            'Óleo de Soja', 'Azeite', 'Bolacha', 'Biscoito', 'Sabonete', 'Shampoo', 'Condicionador', 
            'Detergente', 'Amaciante', 'Sabão em Pó', 'Água Sanitária', 'Desinfetante', 
            'Papel Higiênico', 'Creme Dental', 'Escova de Dentes', 'Fio Dental', 'Desodorante', 
            'Refrigerante', 'Suco', 'Água Mineral', 'Cerveja', 'Vinho', 'Vodka', 'Whisky', 
            'Carne Bovina', 'Frango', 'Peixe', 'Ovos', 'Queijo', 'Presunto', 'Manteiga', 'Margarina', 
            'Iogurte', 'Leite Condensado', 'Creme de Leite', 'Molho de Tomate', 'Maionese', 'Ketchup', 
            'Mostarda', 'Vinagre', 'Sal Grosso', 'Farinha de Mandioca'
        ]

        marcas = [
            'Tio João', 'Camil', 'Dona Benta', 'Pilão', 'Melitta', 'Nestlé', 'Garoto', 'Lacta', 
            'Omo', 'Ypê', 'Brilhante', 'Dove', 'Nivea', 'Rexona', 'Seda', 'Pantene', 'Colgate', 
            'Oral-B', 'Sorriso', 'Coca-Cola', 'Pepsi', 'Guaraná Antarctica', 'Fanta', 'Sprite', 
            'Sadia', 'Perdigão', 'Seara', 'Friboi', 'Aurora', 'Vigor', 'Itambé', 'Piracanjuba', 
            'Elegê', 'Bauducco', 'Marilan', 'Mabel', 'Piraquê', 'Triunfo', 'Adria', 'Renata', 
            'Galo', 'Dona Clara', 'Liza', 'Soya', 'Concórdia', 'Hellmann\'s', 'Heinz', 'Hemmer'
        ]

        variantes = [
            '1kg', '2kg', '5kg', '500g', '200g', '1L', '2L', '1.5L', '900ml', '500ml', '350ml', 
            '200ml', 'Original', 'Integral', 'Desnatado', 'Semidesnatado', 'Diet', 'Light', 'Zero', 
            'Premium', 'Tradicional', 'Extra Forte', 'Suave', 'Crocante', 'Recheado', 'Ao Leite', 
            'Meio Amargo', 'Branco', 'Sem Glúten', 'Sem Lactose'
        ]

        produtos_gerados = []
        nomes_existentes = set()
        
        # Tentar gerar 5000 produtos únicos
        tentativas = 0
        while len(produtos_gerados) < 5000 and tentativas < 50000:
            tentativas += 1
            p = random.choice(produtos_base)
            m = random.choice(marcas)
            v = random.choice(variantes)
            
            nome_completo = f"{p} {m} {v}"
            
            if nome_completo in nomes_existentes:
                continue
                
            nomes_existentes.add(nome_completo)
            
            codigo = fake.unique.ean13()
            quantidade = random.randint(1, 1000)
            preco = round(random.uniform(2.0, 200.0), 2)
            
            produtos_gerados.append(Produto(
                nome=nome_completo,
                codigo=codigo,
                quantidade=quantidade,
                preco=preco
            ))

        Produto.objects.bulk_create(produtos_gerados)
        self.stdout.write(self.style.SUCCESS(f'Banco populado com {len(produtos_gerados)} produtos reais!'))
