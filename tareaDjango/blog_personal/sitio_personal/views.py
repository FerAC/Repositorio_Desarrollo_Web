from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .forms import SubscriptionForm
from django.core.mail import send_mail
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Articulo, Etiqueta, Comentario, Suscripcion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.urls import reverse
from .forms import ContactForm
from .forms import ComentarioForm
from django.conf import settings
from django.http import HttpResponseForbidden
from django.http import JsonResponse

def index(request):
    """
    Vista para la página principal.

    Parámetros:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: La respuesta HTTP con el contenido de la página principal.
    """
    return render(request, 'sitio_personal/index.html')

def blog(request):
    """
    Vista para la página del blog.

    Parámetros:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: La respuesta HTTP con el contenido de la página del blog.
    """
    return render(request, 'sitio_personal/blog.html')

def resume(request):
    """
    Vista para la página del currículum.

    Parámetros:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: La respuesta HTTP con el contenido de la página del currículum.
    """
    return render(request, 'sitio_personal/resume.html')

def about(request):
    """
    Vista para la página de información sobre el sitio.

    Parámetros:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: La respuesta HTTP con el contenido de la página de información.
    """
    return render(request, 'sitio_personal/about.html')

def articulos(request):
    """
    Vista para listar artículos y etiquetas.

    Parámetros:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: La respuesta HTTP con la lista de artículos y etiquetas.
    """
    articulos = Articulo.objects.all()
    etiquetas = Etiqueta.objects.all()
    return render(request, 'sitio_personal/listar_articulos.html', {'articulos': articulos, 'etiquetas': etiquetas})


def listar_articulos(request):
    """
    Vista para listar artículos paginados por popularidad y fecha de publicación.

    Parámetros:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: La respuesta HTTP con los artículos paginados.
    """
    default_page = 1
    page = request.GET.get('page', default_page)
    items_per_page = request.GET.get('items_per_page', 5)

    articulos_por_likes = Articulo.objects.all().order_by('-likes')
    articulos_mas_recientes = Articulo.objects.all().order_by('-fecha_publicacion')

    paginator = Paginator(articulos_por_likes, items_per_page)

    try:
        items_page_likes = paginator.page(page)
    except PageNotAnInteger:
        items_page_likes = paginator.page(default_page)
    except EmptyPage:
        items_page_likes = paginator.page(paginator.num_pages)

    paginator = Paginator(articulos_mas_recientes, items_per_page)

    try:
        items_page_relevant = paginator.page(page)
    except PageNotAnInteger:
        items_page_relevant = paginator.page(default_page)
    except EmptyPage:
        items_page_relevant = paginator.page(paginator.num_pages)

    context = {
        'items_page_likes': items_page_likes,
        'items_page_relevant': items_page_relevant
    }
    return render(request, 'sitio_personal/listar_articulos.html', context)


def contact(request):
    """
    Vista para manejar el formulario de contacto.

    Permite a los usuarios enviar mensajes de contacto. Si el formulario es válido,
    envía un correo electrónico al administrador del sitio y guarda el mensaje en la
    base de datos.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida.

    Retorna:
        HttpResponse: La respuesta HTTP renderizada.
    """
    if request.method == 'POST':
        print("Se va a imprimir metodo")
        print(request.method)
        form = ContactForm(request.POST)
        if form.is_valid():
            print("ENTRA A IF")
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            cuerpo = form.cleaned_data['cuerpo']

            print("Se envia Email")
            # Envío de correo
            send_mail(
                'Nuevo mensaje de contacto',
                f'Nombre: {nombre}\nEmail: {email}\nMensaje:\n{cuerpo}',
                'fer17arce@gmail.com',  # Correo del remitente
                ['fer17arce@gmail.com'],  # Correo del destinatario
                fail_silently=False,
            )
            print("Se envio Email")
            # Guardar el mensaje de contacto en la base de datos
            mensaje_contacto = form.save()
            
            return render(request, 'sitio_personal/contacto_exitoso.html')
        print("------------------------------------------------")
        print(form.errors)
    else:
        print("Entra a else")
        form = ContactForm()
    return render(request, 'sitio_personal/contacto.html', {'form': form})

def detalle_articulo(request, articulo_id):
    """
    Vista para mostrar los detalles de un artículo.

    Obtiene el artículo según su ID y renderiza la plantilla con la información
    del artículo y sus comentarios.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida.
        articulo_id (int): El ID del artículo a mostrar.

    Retorna:
        HttpResponse: La respuesta HTTP renderizada.
    """
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    return render(request, 'sitio_personal/detalle_articulo.html', {'articulo': articulo})

def contact_success(request):
    """
    Vista para mostrar la confirmación de contacto exitoso.

    Renderiza la plantilla de confirmación de contacto exitoso.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida.

    Retorna:
        HttpResponse: La respuesta HTTP renderizada.
    """
    return render(request, 'contact_success.html')

@login_required
def detalle_articulo(request, articulo_id):
    """
    Vista para mostrar los detalles de un artículo y manejar comentarios.

    Obtiene el artículo según su ID, muestra sus detalles y permite a los usuarios
    dejar comentarios en el artículo.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida.
        articulo_id (int): El ID del artículo a mostrar y comentar.

    Retorna:
        HttpResponse: La respuesta HTTP renderizada.
    """
    articulo = get_object_or_404(Articulo, id=articulo_id)
    comentarios = articulo.comentarios.order_by('-fecha').filter(es_respuesta=False)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.articulo = articulo
            comentario.usuario = request.user  # Asigna el usuario autenticado al comentario
            comentario.save()
            return redirect('detalle_articulo', articulo_id=articulo.id)
    else:
        form = ComentarioForm()

    puede_eliminar_comentario = request.user.has_perm('sitio_personal.delete_comentario')

    return render(request, 'sitio_personal/detalle_articulo.html', {
        'articulo': articulo,
        'comentarios': comentarios,
        'form': form,
        'puede_eliminar_comentario': puede_eliminar_comentario,
    })


@login_required
def like_article(request, article_id):
    """
    Vista para gestionar los 'me gusta' en un artículo.

    Permite a los usuarios autenticados dar o quitar 'me gusta' a un artículo.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida.
        article_id (int): El ID del artículo al que se aplica el 'me gusta'.

    Retorna:
        HttpResponseRedirect: La respuesta HTTP de redirección.
    """
    articulo = get_object_or_404(Articulo, id=article_id)
    user = request.user

    # Verificar si el usuario ya le dio 'me gusta' al artículo
    if articulo.likes.filter(id=user.id).exists():
        articulo.likes.remove(user)
    else:
        articulo.likes.add(user)

    return redirect('detalle_articulo', article_id=article_id)

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    articulo_id = comentario.articulo.id
    # Verificar si el usuario tiene permiso para eliminar el comentario
    if request.user == comentario.usuario or request.user.has_perm('sitio_personal.delete_comentario'):
        comentario.delete()
        return redirect('detalle_articulo', articulo_id=articulo_id)
    else:
        return HttpResponseForbidden("No tienes permiso para eliminar este comentario.")

@login_required
def like_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.likes.filter(id=request.user.id).exists():
        comentario.likes.remove(request.user)
        liked = False
    else:
        comentario.likes.add(request.user)
        liked = True
    return JsonResponse({'likes': comentario.likes(),'liked': liked})

def suscribirse(request):
    """
    Vista para manejar el formulario de suscripción.

    Permite a los usuarios suscribirse al blog. Si el formulario es válido,
    crea una nueva suscripción en la base de datos y envía un correo de bienvenida.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida.

    Retorna:
        HttpResponse: La respuesta HTTP renderizada.
    """
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            suscripcion = Suscripcion.objects.create(
                email=form.cleaned_data['email'],
                nombre=form.cleaned_data['nombre'],
                frecuencia=form.cleaned_data['frecuencia'],
                recibir_notificaciones=form.cleaned_data['recibir_notificaciones']
            )
            enviar_correo_bienvenida(form.cleaned_data['email'], form.cleaned_data['nombre'])
            return redirect('suscripcion_exitosa')
    else:
        form = SubscriptionForm()
    return render(request, 'sitio_personal/suscribirse.html', {'form': form})

def suscripcion_exitosa(request):
    """
    Vista para mostrar la confirmación de suscripción exitosa.

    Renderiza la plantilla de confirmación de suscripción exitosa.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida.

    Retorna:
        HttpResponse: La respuesta HTTP renderizada.
    """
    return render(request, 'sitio_personal/suscripcion_exitosa.html')

def enviar_correo_bienvenida(email, nombre):
    """
    Función para enviar un correo de bienvenida a un nuevo suscriptor.

    Envía un correo electrónico de bienvenida al nuevo suscriptor del blog.

    Parámetros:
        email (str): La dirección de correo electrónico del nuevo suscriptor.
        nombre (str): El nombre del nuevo suscriptor.

    Retorna:
        None
    """
    subject = 'Bienvenido a mi Blog'
    message = f'Hola {nombre},\n\nGracias por suscribirte a mi blog. ¡Saludos!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)




