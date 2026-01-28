import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404
from xhtml2pdf import pisa
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

# Vista para la página principal donde pondrás el botón
def home(request):
    # Intentamos obtener el primer perfil creado para el botón de ejemplo
    perfil = DatosPersonales.objects.first()
    return render(request, 'cv/home.html', {'perfil': perfil})

def generar_pdf_cv(request, perfil_id):
    # 1. Obtener todos los datos del perfil específico
    # Usamos get_object_or_404 para que si el ID no existe, envíe un error 404 limpio
    perfil = get_object_or_404(DatosPersonales, idperfil=perfil_id)
    
    # Filtramos los datos relacionados usando el nombre exacto de tus campos FK
    experiencias = ExperienciaLaboral.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    reconocimientos = Reconocimientos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    cursos = CursosRealizados.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    productos_acad = ProductosAcademicos.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)
    productos_lab = ProductosLaborales.objects.filter(idperfilconqueestaactivo=perfil)
    
    # Añadimos la Venta de Garage que creamos
    venta_garage = VentaGarage.objects.filter(idperfilconqueestaactivo=perfil, activarparaqueseveaenfront=True)

    # 2. Preparar el contexto para el HTML
    context = {
        'perfil': perfil,
        'experiencias': experiencias,
        'reconocimientos': reconocimientos,
        'cursos': cursos,
        'productos_acad': productos_acad,
        'productos_lab': productos_lab,
        'venta_garage': venta_garage, # Enviamos los productos de garage al PDF
    }

    # 3. Renderizar el template HTML
    template_path = 'cv/pdf_template.html'
    response = HttpResponse(content_type='application/pdf')
    
    # inline abre el PDF en el navegador, attachment lo descarga directamente
    response['Content-Disposition'] = f'inline; filename="CV_{perfil.apellidos}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    # 4. Crear el PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Ocurrió un error al generar el PDF', status=500)
    
    return response