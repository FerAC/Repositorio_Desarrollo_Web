from django.shortcuts import render
from .forms import SubscriptionForm
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Articulo
from .models import Etiqueta

def index(request):
    return render(request, 'sitio_personal/index.html')

def blog(request):
    
    return render(request, 'sitio_personal/blog.html')

def resume(request):
    return render(request, 'sitio_personal/resume.html')

def about(request):
    return render(request, 'sitio_personal/about.html')

def articulos(request):
    return render(request, 'sitio_personal/listar_articulos.html', {'articulos': articulos, 'etiquetas': etiquetas})

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']
            frecuencia = form.cleaned_data['frecuencia']
            
            
            send_mail(
                'Bienvenido al Blog',
                f'Hola {nombre}, gracias por suscribirte al blog. Estaras recibiendo actualizaciones {frecuencia}.',
                'tu@email.com',
                [email],
                fail_silently=False,
            )

            return render(request, 'suscripcion_exitosa.html', {'nombre': nombre})
    else:
        form = SubscriptionForm()
    return render(request, 'suscripcion.html', {'form': form})

def listar_articulos(request):
    articulos = Articulo.objects.all()
    return render(request, 'sitio_personal/listar_articulos.html', {'articulos': articulos})

def detalle_articulo(request, articulo_id):
    articulo = get_object_or_404(Articulo, pk=articulo_id)
    return render(request, 'detalle_articulo.html', {'articulo': articulo})