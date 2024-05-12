from django.shortcuts import render

def index(request):
    return render(request, 'sitio_personal/index.html')

def blog(request):
    return render(request, 'sitio_personal/blog.html')

def resume(request):
    return render(request, 'sitio_personal/resume.html')

def about(request):
    return render(request, 'sitio_personal/about.html')