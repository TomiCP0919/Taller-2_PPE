from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto
from .forms import FormularioProyecto

def lista_proyectos(request):
    proyectos = Proyecto.objects.all().order_by('-created_at')
    return render(request, 'freelance_hub/lista_proyectos.html', {'proyectos': proyectos})

def crear_proyecto(request):
    if request.method == 'POST':
        form = FormularioProyecto(request.POST)
        if form.is_valid():
            form.save()
            return redirect('freelance_hub:lista_proyectos')
    else:
        form = FormularioProyecto()
    return render(request, 'freelance_hub/crear_proyecto.html', {'form': form, 'es_edicion': False})

def editar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = FormularioProyecto(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('freelance_hub:lista_proyectos')
    else:
        form = FormularioProyecto(instance=proyecto)
    return render(request, 'freelance_hub/crear_proyecto.html', {'form': form, 'es_edicion': True, 'proyecto': proyecto})

def eliminar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('freelance_hub:lista_proyectos')
    return render(request, 'freelance_hub/eliminar_proyecto.html', {'proyecto': proyecto})
