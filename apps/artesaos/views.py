from django.shortcuts import render

from .models import Artesao

# Create your views here.

def listar_artesaos(request):
    artesaos = Artesao.objects.ativos()

    return render(request, 'lista_artesaos.html', {
        'artesaos': artesaos
    })