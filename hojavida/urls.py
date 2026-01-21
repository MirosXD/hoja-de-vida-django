from django.urls import path
from . import views

app_name = "hojavida"

urlpatterns = [
    # Página principal – muestra el perfil activo
    path("", views.home, name="home"),

    # Detalle de un perfil específico
    path(
        "perfil/<int:idperfil>/",
        views.perfil_detalle,
        name="perfil_detalle"
    ),
]

