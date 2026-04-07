from django.urls import path
from . import views

app_name = 'freelance_hub'

urlpatterns = [
    path('', views.lista_proyectos, name='lista_proyectos'),
    path('nuevo_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('editar_proyecto/<int:pk>/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar_proyecto/<int:pk>/', views.eliminar_proyecto, name='eliminar_proyecto'),
]
