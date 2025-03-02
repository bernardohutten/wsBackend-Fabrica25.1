from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Filme, Diretor

def buscar_dados_da_api(titulo):
    url = f"http://www.omdbapi.com/?apikey={settings.OMDB_API_KEY}&t={titulo}"
    resposta = requests.get(url)
    dados = resposta.json()
    return dados

def sincronizar_filme(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        dados = buscar_dados_da_api(titulo)
        
        if dados.get('Response') == 'True':
            diretor_nome = dados.get('Director', 'Desconhecido')
            diretor, criado = Diretor.objects.get_or_create(nome=diretor_nome)
            
            Filme.objects.get_or_create(
                titulo=dados.get('Title'),
                ano=dados.get('Year'),
                diretor=diretor
            )
            return redirect('lista_filmes')
        else:
            return render(request, 'filmes/erro.html', {'mensagem': 'Filme não encontrado na API.'})
    return render(request, 'filmes/sincronizar_filme.html')



from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Filme, Diretor

def lista_filmes(request):
    filmes = Filme.objects.all()
    return render(request, 'filmes/lista_filmes.html', {'filmes': filmes})

def detalhes_filme(request, pk):
    try:
        filme = Filme.objects.get(pk=pk)
        return render(request, 'filmes/detalhes_filme.html', {'filme': filme})
    except ObjectDoesNotExist:
        return render(request, 'filmes/erro.html', {'mensagem': 'Filme não encontrado.'})

def criar_filme(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        ano = request.POST.get('ano')
        diretor_id = request.POST.get('diretor')
        
        try:
            diretor = Diretor.objects.get(id=diretor_id)
            Filme.objects.create(titulo=titulo, ano=ano, diretor=diretor)
            return redirect('lista_filmes')
        except ObjectDoesNotExist:
            return render(request, 'filmes/erro.html', {'mensagem': 'Diretor não encontrado.'})
    
    diretores = Diretor.objects.all()
    return render(request, 'filmes/criar_filme.html', {'diretores': diretores})

def editar_filme(request, pk):
    try:
        filme = Filme.objects.get(pk=pk)
        if request.method == "POST":
            filme.titulo = request.POST.get('titulo')
            filme.ano = request.POST.get('ano')
            diretor_id = request.POST.get('diretor')
            
            try:
                diretor = Diretor.objects.get(id=diretor_id)
                filme.diretor = diretor
                filme.save()
                return redirect('lista_filmes')
            except ObjectDoesNotExist:
                return render(request, 'filmes/erro.html', {'mensagem': 'Diretor não encontrado.'})
        
        diretores = Diretor.objects.all()
        return render(request, 'filmes/editar_filme.html', {'filme': filme, 'diretores': diretores})
    except ObjectDoesNotExist:
        return render(request, 'filmes/erro.html', {'mensagem': 'Filme não encontrado.'})

def deletar_filme(request, pk):
    try:
        filme = Filme.objects.get(pk=pk)
        if request.method == "POST":
            filme.delete()
            return redirect('lista_filmes')
        return render(request, 'filmes/confirmar_delecao_filme.html', {'filme': filme})
    except ObjectDoesNotExist:
        return render(request, 'filmes/erro.html', {'mensagem': 'Filme não encontrado.'})