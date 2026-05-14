"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from apps.artesaos.views import criar_artesao, editar_artesao, listar_artesaos, toggle_ativo
from apps.portal.views import dashboard, home, user_profile

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/", dashboard),
    path("accounts/profile/", user_profile, name="profile"),
    path("artesaos/", listar_artesaos, name="lista_artesaos"),
    path("artesaos/novo/", criar_artesao, name="criar_artesao"),
    path("artesaos/<int:id>/editar/", editar_artesao, name="editar_artesao"),
    path("artesaos/<int:id>/toggle/", toggle_ativo, name="toggle_artesao")
]
