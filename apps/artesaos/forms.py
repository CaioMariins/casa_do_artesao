from django import forms
from .models import Artesao
import re

class ArtesaoForm(forms.ModelForm):
    class Meta:
        model = Artesao
        fields = ['nome', 'descricao', 'categoria', 'telefone', 'ativo']

    def clean(self):
        cleaned_data = super().clean()

        nome = cleaned_data.get('nome')
        categoria = cleaned_data.get('categoria')

        if nome and categoria and nome.lower() == categoria.lower():
            raise forms.ValidationError("Nome não pode ser igual a categoria")
        
        return cleaned_data

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')

        if not nome or not nome.strip():
            raise forms.ValidationError("Nome não pode ser vazio")

        if len(nome) < 3:
            raise forms.ValidationError("Nome muito curto")
        
        return nome
    
    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao')

        if not descricao or len(descricao) < 10:
            raise forms.ValidationError("Descrição muito curta")
        
        return descricao
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        numeros = re.sub(r'\D', '', telefone)

        if len(numeros) not in [10, 11]:
            raise forms.ValidationError("Telefone inválido")
        
        return numeros