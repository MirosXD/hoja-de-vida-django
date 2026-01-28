import os
import django

# Asegúrate de que este nombre coincida con la carpeta que contiene tu settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hoja_vida_django.settings')
django.setup()

from django.contrib.auth.models import User

def create_super():
    username = 'admin'
    email = 'miroslavxde@gmail.com'
    password = 'Miroslav03'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superusuario '{username}' creado exitosamente.")
    else:
        # Si ya existe, le actualizamos la contraseña por si la olvidaste
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"🔄 El usuario '{username}' ya existía. Contraseña actualizada a Miroslav03.")

if __name__ == "__main__":
    create_super()