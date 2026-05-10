from django.db import models

# Create your models here.


class ArtesaoQuerySet(models.QuerySet):
    def ativos(self):
        return self.filter(ativo=True)


class ArtesaoManager(models.Manager):
    def get_queryset(self):
        return ArtesaoQuerySet(self.model, using=self._db)

    def ativos(self):
        return self.get_queryset().ativos()


class Artesao(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    objects = ArtesaoManager()

    def __str__(self):
        return self.nome
