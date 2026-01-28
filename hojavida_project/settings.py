from pathlib import Path
import os
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env
load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------------------
# Seguridad
# ---------------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-me")

# En Render, DJANGO_DEBUG debe ser False (0)
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv(
        "DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,.onrender.com"
    ).split(",")
    if h.strip()
]

# ---------------------------------------------------------------------
# Aplicaciones
# ---------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # Manejo de estáticos optimizado
    "django.contrib.staticfiles",

    # terceros
    "storages",  # django-storages (Azure)

    # apps locales
    "hojavida",  # CORREGIDO: Volvemos al nombre original de tu carpeta
]

# ---------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Necesario para estáticos en Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------------------
# URLs / Templates
# ---------------------------------------------------------------------
ROOT_URLCONF = "hojavida_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media", 
            ],
        },
    },
]

WSGI_APPLICATION = "hojavida_project.wsgi.application"

# ---------------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------------
DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()

if DB_ENGINE == "mssql":
    DATABASES = {
        "default": {
            "ENGINE": "mssql",
            "NAME": os.getenv("AZURE_SQL_DB_NAME", ""),
            "USER": os.getenv("AZURE_SQL_DB_USER", ""),
            "PASSWORD": os.getenv("AZURE_SQL_DB_PASSWORD", ""),
            "HOST": os.getenv("AZURE_SQL_DB_HOST", ""),
            "PORT": os.getenv("AZURE_SQL_DB_PORT", "1433"),
            "OPTIONS": {
                "driver": os.getenv(
                    "AZURE_SQL_ODBC_DRIVER",
                    "ODBC Driver 18 for SQL Server"
                ),
                "extra_params": os.getenv(
                    "AZURE_SQL_EXTRA_PARAMS",
                    "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
                ),
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ---------------------------------------------------------------------
# Internacionalización
# ---------------------------------------------------------------------
LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------
# Archivos estáticos
# ---------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Almacenamiento optimizado para estáticos
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------------------------------------------------------------
# Azure Storage Configuration
# ---------------------------------------------------------------------
AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME", "")
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY", "")
AZURE_CONTAINER = os.getenv("AZURE_CONTAINER", "media")

val_expiration = os.getenv("AZURE_URL_EXPIRATION_SECS", "None")
AZURE_URL_EXPIRATION_SECS = None if val_expiration == "None" else int(val_expiration)

if AZURE_ACCOUNT_NAME and AZURE_ACCOUNT_KEY:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.azure_storage.AzureStorage",
            "OPTIONS": {
                "account_name": AZURE_ACCOUNT_NAME,
                "account_key": AZURE_ACCOUNT_KEY,
                "azure_container": AZURE_CONTAINER,
                "expiration_secs": AZURE_URL_EXPIRATION_SECS,
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    MEDIA_URL = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/'
    MEDIA_ROOT = None 
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------------
# Otros
# ---------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"