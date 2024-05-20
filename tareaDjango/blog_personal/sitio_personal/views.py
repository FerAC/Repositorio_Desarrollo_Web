from django.shortcuts import render, get_object_or_404
from .forms import SubscriptionForm
from django.core.mail import send_mail
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Articulo, Etiqueta, Comentario
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from .forms import ContactForm
from .forms import ComentarioForm

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

def subscribe(request):
    """
    Vista para gestionar suscripciones por correo electrónico.

    Parámetros:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: La respuesta HTTP con el formulario de suscripción o una confirmación de éxito.
    """
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']
            frecuencia = form.cleaned_data['frecuencia']
            
            send_mail(
                'Bienvenido al Blog',
                f'Hola {nombre}, gracias por suscribirte al blog. Estarás recibiendo actualizaciones {frecuencia}.',
                'tu@email.com',
                [email],
                fail_silently=False,
            )
            return render(request, 'suscripcion_exitosa.html', {'nombre': nombre})
    else:
        form = SubscriptionForm()
    return render(request, 'suscripcion.html', {'form': form})

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
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        message = request.POST.get('message')
        
        send_mail(
            'Nuevo mensaje de contacto',
            f'Nombre: {name}\nEmail: {email}\nMensaje:\n{message}',
            'fer17arce@gmail.com',  # Correo del remitente
            ['fer17arce@gmail.com'],  # Correo del destinatario
            fail_silently=False,
        )
        
        return redirect(reverse('contact_success'))  # Utiliza reverse aquí
        
    return render(request, 'contact.html')

def detalle_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    return render(request, 'sitio_personal/detalle_articulo.html', {'articulo': articulo})

def contact_success(request):
    return render(request, 'contact_success.html')

def detalle_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    comentarios = articulo.comentarios.order_by('-fecha').filter(es_respuesta = False)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.articulo = articulo
            comentario.save()
            return redirect('detalle_articulo', articulo_id=articulo.id)
    else:
        form = ComentarioForm()

    return render(request, 'sitio_personal/detalle_articulo.html', {'articulo': articulo, 'comentarios': comentarios, 'form': form})

@login_required
def like_article(request, article_id):
    articulo = get_object_or_404(Articulo, id=article_id)
    user = request.user

    # Verificar si el usuario ya le dio 'me gusta' al artículo
    if articulo.likes.filter(id=user.id).exists():
        articulo.likes.remove(user)
    else:
        articulo.likes.add(user)

    return redirect('detalle_articulo', article_id=article_id)

