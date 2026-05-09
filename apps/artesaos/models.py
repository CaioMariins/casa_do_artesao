from django.db import models

# Create your models here.


class ArtesaoQuerySet(models.QuerySet):
    def ativos(self):
        return self.filter(ativo=True)


class Artesao(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    objects = ArtesaoQuerySet.as_manager()

    def __str__(self):
        return self.nome
