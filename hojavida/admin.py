from django.contrib import admin
from django.utils.html import format_html
from .models import (
    DatosPersonales, ExperienciaLaboral, ProductosLaborales, 
    Reconocimientos, CursosRealizados, ProductosAcademicos, VentaGarage
)

# Configuración del encabezado del panel
admin.site.site_header = "Administración de Hoja de Vida"
admin.site.index_title = "Módulos de Currículum"

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    # 'get_sexo' mostrará el texto formateado en la lista
    list_display = (
        "idperfil", 
        "apellidos", 
        "nombres", 
        "numerocedula", 
        "get_sexo", 
        "licenciaconducir", 
        "perfilactivo"
    )
    search_fields = ("apellidos", "nombres", "numerocedula")
    
    # Filtros actualizados: se cambió 'sexo_masculino' por 'sexo'
    list_filter = ("sexo", "nacionalidad", "perfilactivo", "licenciaconducir")
    ordering = ('apellidos',)

    @admin.display(description="Sexo")
    def get_sexo(self, obj):
        """Traduce los códigos M/F a texto legible en la lista"""
        if obj.sexo == 'M':
            return "Masculino"
        elif obj.sexo == 'F':
            return "Femenino"
        return "No definido"

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ("idexperiencialaboral", "nombrempresa", "cargodesempenado", "fechainiciogestion", "fechafingestion", "perfil")
    search_fields = ("nombrempresa", "cargodesempenado", "perfil__apellidos", "perfil__nombres")
    list_filter = ("activarparaqueseveaenfront", "fechainiciogestion")
    raw_id_fields = ("perfil",)

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ("idproductoslaborales", "nombreproducto", "fechaproducto", "perfil")
    search_fields = ("nombreproducto", "perfil__apellidos")
    raw_id_fields = ("perfil",)

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ("idreconocimiento", "tiporeconocimiento", "institucioncertificado", "fechareconocimiento", "perfil")
    search_fields = ("tiporeconocimiento", "institucioncertificado", "perfil__apellidos")
    list_filter = ("activarparaqueseveaenfront", "fechareconocimiento")
    raw_id_fields = ("perfil",)

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ("idcursorealizado", "nombrecurso", "totalhoras", "fechainicio", "fechafin", "perfil")
    search_fields = ("nombrecurso", "perfil__apellidos")
    list_filter = ("activarparaqueseveaenfront",)
    raw_id_fields = ("perfil",)

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ("idproductoacademico", "nombreproducto", "fechaproducto", "perfil")
    search_fields = ("nombreproducto", "perfil__apellidos")
    list_filter = ("activarparaqueseveaenfront",)
    raw_id_fields = ("perfil",)

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ("idventagarage", "nombreproducto", "valordelbien", "estadoproducto", "perfil")
    search_fields = ("nombreproducto", "perfil__apellidos")
    list_filter = ("estadoproducto", "activarparaqueseveaenfront")
    raw_id_fields = ("perfil",)