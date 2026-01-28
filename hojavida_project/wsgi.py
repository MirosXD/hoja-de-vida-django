import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hojavida_project.settings")
application = get_wsgi_application()

# Al final de wsgi.py
from django.contrib.auth.models import User

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@ejemplo.com', 'Miroslav03')
        print("✅ ADMIN CREADO DESDE WSGI")
    else:
        user = User.objects.get(username='admin')
        user.set_password('Miroslav03')
        user.save()
        print("🔄 PASSWORD DE ADMIN ACTUALIZADA")
except Exception as e:
    print(f"Error creando admin: {e}")