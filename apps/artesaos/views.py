from django.shortcuts import render, redirect
from .forms import ArtesaoForm
from .models import Artesao

# Create your views here.

def listar_artesaos(request):
    artesaos = Artesao.objects.ativos()

    return render(request, 'artesaos/lista_artesaos.html', {
        'artesaos': artesaos
    })


def criar_artesao(request):
    form = ArtesaoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_artesaos')
    
    return render(request, 'artesaos/form.html', {
        'form': form
    })
