from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Importante
from django.conf.urls.static import static  # Importante

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("hojavida.urls", namespace="hojavida")),
]

# ESTA PARTE ES LA QUE SOLUCIONA EL ERROR DE LAS IMÁGENES:
# Solo se activa en modo desarrollo (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
