from django.shortcuts import render, get_object_or_404
from .models import DatosPersonales
from .utils import generar_sas_blob
import logging

# Configuración de logs por si hay errores en Azure
logger = logging.getLogger(__name__)

def home(request):
    """
    Página principal que lista los perfiles con manejo de fotos seguro.
    """
    perfiles = DatosPersonales.objects.all().order_by("-idperfil")

    for p in perfiles:
        # 1. Definimos un placeholder profesional (Avatar con iniciales) si no hay foto
        p.foto_safe_url = f"https://ui-avatars.com/api/?name={p.nombres}+{p.apellidos}&background=0d1411&color=10b981&size=128"
        
        if p.foto:
            try:
                # 2. Intentamos obtener la URL de Azure o Local
                # p.foto.url funcionará correctamente gracias a la configuración de settings.py
                p.foto_safe_url = p.foto.url
            except Exception as e:
                logger.error(f"Error al obtener URL de foto para perfil {p.idperfil}: {e}")
                # Si falla (ej. error de padding en Python 3.13), se mantiene el avatar de arriba
                pass

    return render(request, "hojavida/home.html", {"perfiles": perfiles})

def perfil_detalle(request, idperfil: int):
    """
    Vista detallada con soporte para certificados privados mediante tokens SAS.
    """
    perfil = get_object_or_404(DatosPersonales, idperfil=idperfil)
    
    # Filtramos solo los datos activos para el front-end
    experiencias = perfil.experiencias_laborales.filter(activarparaqueseveaenfront=True)
    cursos = perfil.cursos_realizados.filter(activarparaqueseveaenfront=True)
    reconocimientos = perfil.reconocimientos.filter(activarparaqueseveaenfront=True)

    # Manejo de certificados en Reconocimientos
    for r in reconocimientos:
        r.sas_url = ""
        if r.fotocertificado:
            try:
                # Intentamos generar URL temporal si estamos en Azure
                # Si estamos en local, usamos la URL normal del archivo
                if hasattr(r.fotocertificado.storage, 'connection_string'):
                    r.sas_url = generar_sas_blob(r.fotocertificado.name)
                else:
                    r.sas_url = r.fotocertificado.url
            except Exception as e:
                logger.warning(f"No se pudo generar SAS para certificado: {e}")
                r.sas_url = r.fotocertificado.url if r.fotocertificado else ""

    contexto = {
        "perfil": perfil,
        "experiencias": experiencias,
        "cursos": cursos,
        "reconocimientos": reconocimientos,
    }
    return render(request, "hojavida/perfil_detalle.html", contexto)