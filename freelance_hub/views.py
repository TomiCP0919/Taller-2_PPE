from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Case, When, Value, IntegerField
from .models import Proyecto
from .forms import FormularioProyecto

def landing_page(request):
    return render(request, 'freelance_hub/landing.html')

def lista_proyectos(request):
    proyectos = Proyecto.objects.all()

    # 1. Recuperar parámetros GET
    q = request.GET.get('q', '')
    cliente = request.GET.get('cliente', '')
    estado_filtro = request.GET.get('estado', '')

    # 2. Aplicar Filtros (si existen)
    if q:
        proyectos = proyectos.filter(nombre__icontains=q)
    if cliente:
        proyectos = proyectos.filter(cliente__icontains=cliente)
    if estado_filtro:
        proyectos = proyectos.filter(estado=estado_filtro)

    # 3. Aplicar Ordenamiento Avanzado (Prioridad Alta -> Media -> Baja, luego por ID)
    proyectos = proyectos.annotate(
        prioridad_peso=Case(
            When(prioridad='Alta', then=Value(1)),
            When(prioridad='Media', then=Value(2)),
            When(prioridad='Baja', then=Value(3)),
            output_field=IntegerField(),
        )
    ).order_by('prioridad_peso', 'id')

    context = {
        'proyectos': proyectos,
        'q': q,
        'cliente': cliente,
        'estado_filtro': estado_filtro
    }
    return render(request, 'freelance_hub/lista_proyectos.html', context)

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
