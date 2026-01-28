from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "hojavida"

urlpatterns = [
    # Página principal que lista los perfiles
    path("", views.home, name="home"),

    # Apartado propio para el catálogo general de ventas
    path("venta-garage/", views.lista_venta_garage, name="lista_venta_garage"),

    # NUEVA RUTA: Detalle de un objeto específico de la venta de garage
    # Esto permite ver la información e imagen de un producto individualmente
    path("venta-garage/articulo/<int:id_item>/", views.detalle_objeto_garage, name="detalle_objeto_garage"),

    # Vista detallada de la hoja de vida en la web (Donde ahora sale la tabla de Cursos)
    path("perfil/<int:idperfil>/", views.perfil_detalle, name="perfil_detalle"),

    # Ruta para descargar el PDF corregido con el campo valordelbien
    path("pdf/<int:perfil_id>/", views.generar_pdf_cv, name="generar_pdf_cv"),

] 

# Configuración para servir archivos multimedia (fotos de perfil, productos, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)