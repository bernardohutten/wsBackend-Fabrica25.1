from django.db import models

# Create your models here.
class Diretor(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    ano = models.CharField(max_length=4)
    diretor = models.ForeignKey(Diretor, on_delete=models.CASCADE, related_name='filmes')

    def __str__(self):
        return self.titulo