from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import (
    DatosPersonales, 
    ExperienciaLaboral, 
    CursosRealizados, 
    Reconocimientos,
    VentaGarage,  
    ProductosLaborales,
    ProductosAcademicos
)
from .utils import generar_sas_blob
import logging

logger = logging.getLogger(__name__)

def home(request):
    perfiles = DatosPersonales.objects.all().order_by("-idperfil")
    for p in perfiles:
        p.foto_safe_url = f"https://ui-avatars.com/api/?name={p.nombres}+{p.apellidos}&background=0d1411&color=10b981&size=128"
        if p.foto:
            try:
                p.foto_safe_url = p.foto.url
            except Exception as e:
                logger.error(f"Error cargando foto de perfil {p.idperfil}: {e}")
        
        p.sexo_texto = "Hombre" if p.sexo == "M" else "Mujer"
    return render(request, "hojavida/home.html", {"perfiles": perfiles})

def lista_venta_garage(request):
    productos = VentaGarage.objects.filter(activarparaqueseveaenfront=True).order_by("-idventagarage")
    # Aseguramos que las miniaturas en la lista general también tengan SAS
    for p in productos:
        p.sas_url = generar_sas_blob(p.foto.name) if p.foto else None
    return render(request, "hojavida/venta_garage.html", {"productos": productos})

def detalle_objeto_garage(request, id_item):
    articulo = get_object_or_404(VentaGarage, idventagarage=id_item)
    articulo.sas_url = generar_sas_blob(articulo.foto.name) if articulo.foto else None
    return render(request, "hojavida/detalle_objeto.html", {"articulo": articulo})

def obtener_datos_raw(tabla, id_perfil):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({tabla})")
        columnas_reales = [row[1] for row in cursor.fetchall()]
        posibles_nombres = ['idperfilconqueestaactivo', 'idperfil', 'idperfil_id', 'perfil_id', 'datos_personales_id']
        columna_encontrada = next((nombre for nombre in posibles_nombres if nombre in columnas_reales), None)
        if not columna_encontrada: return []
        query = f'SELECT * FROM {tabla} WHERE {columna_encontrada} = %s'
        cursor.execute(query, [id_perfil])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def perfil_detalle(request, idperfil: int):
    perfil = get_object_or_404(DatosPersonales, idperfil=idperfil)
    
    # Obtenemos datos raw
    experiencias = obtener_datos_raw("experiencialaboral", idperfil)
    cursos = obtener_datos_raw("cursosrealizados", idperfil)
    reconocimientos = obtener_datos_raw("reconocimientos", idperfil)
    
    # Querysets normales para productos
    productos_lab = ProductosLaborales.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
    productos_aca = ProductosAcademicos.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
    venta_garage_items = VentaGarage.objects.filter(perfil=perfil)

    perfil.sexo_texto = "Hombre" if perfil.sexo == "M" else "Mujer"
    perfil.licencia_texto = "Sí" if perfil.licenciaconducir == "Si" else "No"

    # --- GENERACIÓN DE SAS URLS PARA CADA SECCIÓN ---

    # 1. SAS para Experiencias (Raw data utiliza diccionarios)
    for e in experiencias:
        ruta = e.get('rutacertificado')
        e['sas_url'] = generar_sas_blob(ruta) if ruta else ""

    # 2. SAS para Cursos (Raw data)
    for c in cursos:
        ruta = c.get('rutacertificado')
        c['sas_url'] = generar_sas_blob(ruta) if ruta else ""

    # 3. SAS para Reconocimientos (Raw data)
    for r in reconocimientos:
        ruta = r.get('rutacertificado') or r.get('fotocertificado')
        r['sas_url'] = generar_sas_blob(ruta) if ruta else ""

    # 4. SAS para Productos Laborales (Queryset usa objetos)
    for pl in productos_lab:
        pl.sas_url = generar_sas_blob(pl.foto_producto.name) if pl.foto_producto else None

    # 5. SAS para Productos Académicos
    for pa in productos_aca:
        pa.sas_url = generar_sas_blob(pa.foto_producto.name) if pa.foto_producto else None

    contexto = {
        "perfil": perfil, 
        "experiencias": experiencias, 
        "cursos": cursos,
        "reconocimientos": reconocimientos, 
        "venta_garage": venta_garage_items,
        "productos_laborales": productos_lab, 
        "productos_academicos": productos_aca,
    }
    return render(request, "hojavida/perfil_detalle.html", contexto)

def generar_pdf_cv(request, perfil_id):
    perfil = get_object_or_404(DatosPersonales, idperfil=perfil_id)
    experiencias = obtener_datos_raw("experiencialaboral", perfil_id)
    cursos = obtener_datos_raw("cursosrealizados", perfil_id)
    reconocimientos_qs = Reconocimientos.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
    productos_lab = ProductosLaborales.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
    productos_aca = ProductosAcademicos.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)
    venta_garage = VentaGarage.objects.filter(perfil=perfil, activarparaqueseveaenfront=True)

    perfil.sexo_texto = "Hombre" if perfil.sexo == "M" else "Mujer"
    perfil.licencia_texto = "Sí" if perfil.licenciaconducir == "Si" else "No"
    foto_perfil_url = generar_sas_blob(perfil.foto.name) if perfil.foto else None

    # Reconocimientos PDF
    reconocimientos_lista = []
    for r in reconocimientos_qs:
        ruta_img = r.fotocertificado.name if r.fotocertificado else (r.rutacertificado.name if r.rutacertificado else None)
        reconocimientos_lista.append({
            'tiporeconocimiento': r.tiporeconocimiento,
            'institucioncertificado': r.institucioncertificado,
            'fechareconocimiento': r.fechareconocimiento,
            'sas_url': generar_sas_blob(ruta_img) if ruta_img else None
        })

    # SAS para productos en PDF
    for pl in productos_lab:
        pl.sas_url = generar_sas_blob(pl.foto_producto.name) if pl.foto_producto else None
    for pa in productos_aca:
        pa.sas_url = generar_sas_blob(pa.foto_producto.name) if pa.foto_producto else None
    for item in venta_garage:
        item.sas_url = generar_sas_blob(item.foto.name) if item.foto else None
        item.precio_display = f"{item.valordelbien:.2f}" if item.valordelbien else "0.00"

    contexto = {
        "perfil": perfil, "experiencias": experiencias, "cursos": cursos,
        "reconocimientos": reconocimientos_lista, "productos_laborales": productos_lab,
        "productos_academicos": productos_aca, "venta_garage": venta_garage,
        "foto_perfil_url": foto_perfil_url,
    }

    response = HttpResponse(content_type='application/pdf')
    filename = f"CV_{perfil.apellidos}_{perfil.nombres}.pdf".replace(" ", "_")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    template = get_template('hojavida/pdf_template.html')
    html = template.render(contexto)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err: return HttpResponse('Error al generar el PDF', status=500)
    return response