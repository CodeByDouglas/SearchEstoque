from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=255, db_index=True)
    codigo = models.CharField(max_length=50, unique=True)
    quantidade = models.IntegerField(default=0)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome
