from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_filmes, name='lista_filmes'),
    path('sincronizar/', views.sincronizar_filme, name='sincronizar_filme'),
    path('filme/<int:pk>/', views.detalhes_filme, name='detalhes_filme'),
    path('filme/novo/', views.criar_filme, name='criar_filme'),
    path('filme/<int:pk>/editar/', views.editar_filme, name='editar_filme'),
    path('filme/<int:pk>/deletar/', views.deletar_filme, name='deletar_filme'),
]