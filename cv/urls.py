from django.urls import path
from . import views

# Este es el nombre que usaremos para referenciar las rutas de esta app
app_name = 'cv' 

urlpatterns = [
    # Página principal (donde pondremos el botón)
    path('', views.home, name='home'),
    
    # Ruta para generar el PDF
    path('pdf/<int:perfil_id>/', views.generar_pdf_cv, name='generar_pdf_cv'),
]