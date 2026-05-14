from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArtesaoForm
from .models import Artesao

# Create your views here.


def listar_artesaos(request):
    mostrar_inativos = request.GET.get("inativos")

    if mostrar_inativos:
        artesaos = Artesao.objects.all()
    else:
        artesaos = Artesao.objects.ativos()

    return render(request, "artesaos/lista_artesaos.html", {"artesaos": artesaos})


def criar_artesao(request):
    form = ArtesaoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lista_artesaos")

    return render(request, "artesaos/form.html", {"form": form})


def editar_artesao(request, id):
    artesao = get_object_or_404(Artesao, id=id)

    form = ArtesaoForm(request.POST or None, instance=artesao)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("lista_artesaos")

    return render(request, "artesaos/form.html", {"form": form})


def toggle_ativo(request, id):
    artesao = get_object_or_404(Artesao, id=id)

    artesao.ativo = not artesao.ativo
    artesao.save()

    return redirect("lista_artesaos")
