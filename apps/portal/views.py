from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def home(request):
    return HttpResponse("Sistema funcionando")

@staff_member_required
def dashboard(request):
    return HttpResponse("<h1>Área administrativa</h1>")

