from django.contrib import admin
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimiento,
    CursoRealizado,
    ProductoAcademico,
    ProductoLaboral,
    VentaGarage,
)


@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = (
        "idperfil",
        "apellidos",
        "nombres",
        "numerocedula",
        "perfilactivo",
    )
    search_fields = ("apellidos", "nombres", "numerocedula")
    list_filter = ("perfilactivo",)


@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = (
        "idexperiencialaboral",  # ✅ NOMBRE CORRECTO
        "perfil",
        "cargodesempenado",
        "nombrempresa",
        "activarparaqueseveaenfront",
    )
    list_filter = ("activarparaqueseveaenfront",)
    search_fields = ("cargodesempenado", "nombrempresa")


@admin.register(Reconocimiento)
class ReconocimientoAdmin(admin.ModelAdmin):
    list_display = (
        "idreconocimiento",
        "perfil",
        "tiporeconocimiento",
        "fechareconocimiento",
        "activarparaqueseveaenfront",
    )
    list_filter = ("tiporeconocimiento", "activarparaqueseveaenfront")


@admin.register(CursoRealizado)
class CursoRealizadoAdmin(admin.ModelAdmin):
    list_display = (
        "idcursorealizado",
        "perfil",
        "nombrecurso",
        "totalhoras",
        "activarparaqueseveaenfront",
    )
    list_filter = ("activarparaqueseveaenfront",)


@admin.register(ProductoAcademico)
class ProductoAcademicoAdmin(admin.ModelAdmin):
    list_display = (
        "idproductoacademico",
        "perfil",
        "nombreproducto",
        "activarparaqueseveaenfront",
    )


@admin.register(ProductoLaboral)
class ProductoLaboralAdmin(admin.ModelAdmin):
    list_display = (
        "idproductoslaborales",
        "perfil",
        "nombreproducto",
        "activarparaqueseveaenfront",
    )


@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = (
        "idventagarage",
        "perfil",
        "nombreproducto",
        "estadoproducto",
        "valordelbien",
        "activarparaqueseveaenfront",
    )
    list_filter = ("estadoproducto",)
