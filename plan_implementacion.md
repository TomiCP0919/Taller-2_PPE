# Plan de Implementación: Freelance Hub (CRUD en Django)

## Descripción del Objetivo
Construir un sistema de gestión de proyectos freelance ("Freelance Hub") implementando de manera estricta la arquitectura MVT (Model-View-Template) de Django. El sistema permitirá realizar un CRUD completo (Crear, Leer, Actualizar, Eliminar) sobre una entidad `proyecto`.

---

## 1. Estructura del Proyecto

### Creación del Proyecto y la App
Para iniciar, se utilizarán los comandos de consola de Django:
1. `django-admin startproject mi_proyecto .` (crea el proyecto principal en la carpeta actual).
2. `python manage.py startapp freelance_hub` (crea la aplicación específica para gestionar los proyectos).
3. Registrar la app `freelance_hub` dentro del archivo `mi_proyecto/settings.py` en la lista `INSTALLED_APPS`.

### Organización de Carpetas
Bajo el paradigma MVT, la estructura interna debe reflejar claramente las responsabilidades:
```text
mi_proyecto/          # Configuración global del proyecto (settings, urls raíz)
    urls.py             # Enrutamiento específico de esta pequeña app
freelance_hub/              # Nuestra aplicación principal
    models.py           # (M) Modelos de datos (base de datos)
    views.py            # (V) Lógica de negocio (controladores)
    forms.py            # Clases de ModelForm para capturar datos
    templates/          # (T) Interfaz de usuario HTML
            base.html           # Plantilla maestra
            lista_proyectos.html  # Read: Dashboard principal
            crear_proyecto.html  # Create/Update: Formulario
            eliminar_proyecto.html # Delete: Mensaje de confirmación
    migrations/         # Migraciones de la base de datos
```

---

## 2. Diseño del Modelo (`models.py`)

El modelo `proyecto` será la clase que representa la tabla en la base de datos SQL.

### Campos y Razonamiento
* **`id`**: `AutoField()` - Identificador único del proyecto.
* **`created_at`**: `DateTimeField(auto_now_add=True)` - Fecha de creación del proyecto.
* **`updated_at`**: `DateTimeField(auto_now=True)` - Fecha de actualización del proyecto.
* **`nombre`**: `CharField()` - Texto corto para el título o nombre del proyecto freelance.
* **`cliente`**: `CharField()` - Nombre del cliente contratante.
* **`descripcion`**: `TextField()` - Texto largo para detalles específicos, alcances y requerimientos.
* **`presupuesto`**: `DecimalField()` - Ideal para manejar transacciones económicas sin problemas de redondeo (Ej. `max_digits=10, decimal_places=2`).
* **`fecha_inicio`**: `DateField()` - Fecha de inicio del proyecto.
* **`fecha_limite`**: `DateField()` - Fecha esperada de entrega (DeadLine).
* **`prioridad`**: `CharField()` - Usando el atributo `choices` restringiremos limitando opciones a tuplas predefinidas ('Baja', 'Media', 'Alta').
* **`estado`**: `CharField()` - Igualmente con `choices` (P.ej. 'Pendiente', 'En Progreso', 'Completado').

### Migraciones
Tras codificar el modelo en python, se sincroniza con el motor de base de datos a través de los ORM de Django:
1. `python manage.py makemigrations` (Traduce el código Python a un "script SQL ficticio").
2. `python manage.py migrate` (Ejecuta el script SQL para crear efectivamente la tabla `proyectos_proyecto`).

---

## 3. Formularios (`forms.py`)

Para no construir la estructura HTML `<form>` a mano, Django nos ofrece `ModelForm`. 
Crearemos un archivo `forms.py` (no viene por defecto) y dentro una clase `FormularioProyecto` que hereda de `forms.ModelForm`.

* **Configuración Clave (`class Meta`)**:
  * **`model = proyecto`**: Le dice a Django "Crea un formulario basándote en esta tabla".
  * **`fields = '__all__'`**: Incluye masivamente todos los campos editables, exceptuando identificadores ocultos como el ID.
  * **`widgets`**: Un diccionario que te permite inyectar utilidades visuales desde Python. Aquí asignaremos la clase `form-control` de bootstrap a todos los inputs y convertiremos la Fecha Límite y Fecha de inicio visualmente a un calendario HTML5 (`type="date"`).

---

## 4. Vistas (`views.py`) - Explicación de la lógica

La Vista es el "cerebro" o controlador del patrón MVT. Recibe un pedido http, extrae cosas de un modelo y se lo empuja al template correcto.

* **Listar Proyectos (Read - `lista_proyectos`)**:
  * Consulta toda la DB: `proyectos = proyecto.objects.all()`.
  * Empaca la variable `proyectos` como diccionario ("context") y la envía al archivo `lista_proyectos.html`.
* **Crear Proyecto (Create - `crear_proyecto`)**:
  * Maneja 2 situaciones:
    * *Si el usuario entra normal (GET):* Le mandamos el template `crear_proyecto.html` con un formulario vacío instanciado en Python.
    * *Si el usuario clica el botón submit (POST):* Recoge los datos que viajaron. Ejecuta `.is_valid()`. Si está correcto y nadie hackeó los campos, lanza `.save()` e inmediatamente lo redirige hacia el listado `lista_proyectos`.
* **Editar Proyecto (Update - `editar_proyecto`)**:
  * Parecido a Create, pero por la URL recibe un ID (`pk` / `Primary Key`).
  * Con este `pk`, la vista recupera el producto original de la base de datos y se lo adjunta al formulario: `formulario_proyecto(instance=proyecto_actual)`. Así, al mandarlo al template `crear_proyecto.html`, los campos no están vacíos sino pre-llenados.
* **Eliminar (Delete - `eliminar_proyecto`)**:
  * Busca el ID del proyecto respectivo.
  * Por GET lo manda a `eliminar_proyecto.html` consultando si está seguro.
  * Por POST (al clicar botón rojo de confirmar) ejecuta `proyecto.delete()` y manda de vuelta a la lista. 

---

## 5. Rutas / URLs (`urls.py`)

Debemos conectar cada Vista con una "URL Web" en particular. Dividiremos los enrutadores para hacerlo escalable, delegando desde `freelance_hub/urls.py` hacia un interno `proyectos/urls.py`.

* **Estructura amigable de las URLs de la App**:
  * `''` (Raíz de la web) -> Invoca Vista `lista_proyectos` (Name: 'lista_proyectos')
  * `'nuevo_proyecto/'` -> Invoca Vista `crear_proyecto` (Name: 'crear_proyecto')
  * `'editar_proyecto/<int:pk>/'` -> Invoca Vista `editar_proyecto` (Name: 'editar_proyecto'). El `<int:pk>` captura un número como variable.
  * `'eliminar_proyecto/<int:pk>/'` -> Invoca Vista `eliminar_proyecto` (Name: 'eliminar_proyecto')

*Se implementa siempre el argumento `name=` para poder referenciar dinámicamente las rutas dentro de los botones HTML, independientemente de si la url "física" cambia en el futuro.*

---

## 6. Templates (Las interfaces)

Tienen extensión `.html` pero usan DTL (Django Template Language) simbolizado con llaves `{{ variable }}` para mostrar datos e `{% if %}` / `{% for %}` para ejecución de lógica en el front.

* **`base.html`**: El archivo "Padre". Contendrá la estructura `<html>`, `<head>`, librerías CDN importadas (Bootstrap), y las barras de navegación principales. Poseerá una etiqueta vacía llamada `{% block content %}{% endblock %}` que se comportará como un agujero negro que los demás componentes llenarán.
* **`lista_proyectos.html`**: Construye dentro de un `{% for %}` las filas de una `<table class='table'>`. Tiene botones enlazados con sus PKs a la vista de "Editar" y "Eliminar".
* **`crear_proyecto.html`**: Recicla el formulario y lo procesa. El formulario se imprime solo con renderizar `{{ form.as_p }}`. Contendrá la indispensable etiqueta `{% csrf_token %}` por seguridad.
* **`eliminar_proyecto.html`**: Un aviso en pantalla gigante para prevenir los molestos "miss-clicks" o que crawlers web de bots accidentalmente borren datos de DB pulsando enlaces. Solo con un envío de `<form method="POST">` este confirmará el borrado.

---

## 7. Estilos e Integración Visual (Bootstrap)

* **Importación única**: Se pondrá el CSS y JS CDN de Bootstrap 5 estrictamente dentro de `base.html`.
* **Grillas Integradas**: El dashboard usará `.container`, `.row`, y `.col` para ser adaptable a móviles.
* **Uso de Colores Lógicos**: 
  * Un bloque visual If/Else en DTL aplicará badges con clases semánticas de acuerdo a la cadena de texto de la base de datos.
  * Ejemplo en prioridades: `Alta = .bg-danger`, `Media = .bg-warning`, `Baja = .bg-success`.
  * Status: `Pendiente = txt-primary`, `En progreso = txt-warning`, `Completado = txt-success`.
* **Botones intencionales**: Botones para crear (`btn-primary`), para guardar o validar (`btn-success`) y para acciones destructivas (`btn-danger`).

---

## 8. Flujo o Viaje Completo del Sistema ("User Journey")

1. **Visita a Lista**: El usuario llega al dominio raíz. El URL Catcher direcciona a la vista `lista_proyectos`, extrae 5 proyectos de DB, renderiza el template `lista_proyectos.html` con una tabla.
2. **Acción Nuevo**: Usuario pulsa botón azul "+ Nuevo". La vista lanza `crear_proyecto.html`. Él llena y pulsa botón Verde "Guardar". Pasa por POST a la vista, se valida que todo tipo de dato esté sano, guarda en DB y hace "Redirect" de forma segura de retorno a la tabla.
3. **Acción Editar**: Usuario nota un error en el proyecto 3. Pulsa botón Amarillo de la fila respectiva que apunta a `/editar_proyecto/3/`. Entra y los datos ya están allí pre-cargados. Acomoda el título, guarda, y es retornado a la lista modificado.
4. **Acción Eliminar**: Proyecto 1 está inválido. Pulsa botón Rojo, la app lo envía a `/eliminar_proyecto/1/`. La pantalla exige confirmación. Repulsa el rojo, y un Redirect lo retorna confirmando el ID 1 ya muerto.

---

## 9. Buenas Prácticas a Considerar al programar

* **Namespacing en Rutas (`app_name = "proyectos"`)**: Facilita usar la convención `{% url 'proyectos:lista' %}` que salva tu código ante la alta probabilidad de que 2 apps tengan una ruta "lista".
* **Manejo de Objeto No Existente**: En Update o Delete, si la url `/editar_proyecto/999/` es incrustada y el ID 999 no existe: Usaremos la función encapsuladora `get_object_or_404(Proyecto, pk=pk)`, que en caso de error expone un 404 de página no encontrada bonito con un mensaje que le avise al usuario que dicho proyecto no exite, para que el usuario en lugar de colapsar terminales 500 con error a nivel servidor de sistema.
* **Seguridad Obligatoria CSRF**: Ningún `<form>` funcionará sin inyectar la directiva `{% csrf_token %}` en su estructura; Django bloqueará la operación. Protege de Cross-Site Request Forgery.
* **Nomenclatura (Regla PEP-8)**:
  * Modelos/Clases/Formularios: Nombre Singular y UpperCamelCase (`Proyecto` / `FormularioProyecto`).
  * Variables/Funciones/Vistas: snake_case (`mi_proyecto`, `lista_proyectos`).

---
> [!NOTE] 
> User Review Required:
> ¿Qué te parece este nivel de detalle para el plan del proyecto "Freelance Hub"? ¿Te sientes cómodo con la lógica conceptual descrita o necesitas que explique en el plan cómo funcionaría la misma arquitectura usando vistas basadas en clases integradas (Class-Based Views genéricas) en lugar del esquema tradicional mencionado aquí?
