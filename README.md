# Proyecto Hoja de Vida (Django)

Este ZIP incluye un proyecto Django listo para ejecutar, con **todas las tablas** del archivo Excel:
- DATOSPERSONALES
- EXPERIENCIALABORAL
- RECONOCIMIENTOS
- CURSOSREALIZADOS
- PRODUCTOSACADEMICOS
- PRODUCTOSLABORALES
- VENTAGARAGE

Incluye:
- Modelos Django con llaves foráneas (relación a `DatosPersonales`)
- Admin para cargar datos fácil
- Vista mínima: lista de perfiles y detalle del perfil

## 1) Crear entorno virtual e instalar dependencias (desde cero)

> **Windows (PowerShell)**
```powershell
cd hojavida_project
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Linux/Mac**
```bash
cd hojavida_project
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2) Variables de entorno (.env)

1. Copia `.env.example` a `.env`
2. Por defecto el proyecto usa SQLite para que puedas correrlo inmediato.

## 3) Migraciones y ejecutar

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Admin: `http://127.0.0.1:8000/admin/`
- Sitio: `http://127.0.0.1:8000/`

## 4) Conectar a Azure SQL Database (SQL Server)

### A) Pre-requisitos
- Tener creado el **Azure SQL Database** y permitir tu IP en el Firewall del servidor.
- Instalar un driver ODBC:
  - Windows: **ODBC Driver 18 for SQL Server**
  - Linux: msodbcsql18 (según tu distro)

### B) Configurar `.env`
En tu `.env`:
```ini
DB_ENGINE=mssql
AZURE_SQL_DB_HOST=tu-servidor.database.windows.net
AZURE_SQL_DB_PORT=1433
AZURE_SQL_DB_NAME=tu_base
AZURE_SQL_DB_USER=tu_usuario
AZURE_SQL_DB_PASSWORD=tu_password
AZURE_SQL_ODBC_DRIVER=ODBC Driver 18 for SQL Server
AZURE_SQL_EXTRA_PARAMS=Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
```

### C) Migrar en Azure
```bash
python manage.py migrate
```

## Notas
- Los campos `activarparaqueseveaenfront` están como `BooleanField(default=True)` tal como `DEFAULT 1`.
- Las restricciones `CHECK` se manejan con `choices` en Django.
