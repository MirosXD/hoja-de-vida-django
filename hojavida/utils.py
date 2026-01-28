from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
import os

def generar_sas_blob(blob_name: str) -> str:
    """
    Devuelve una URL firmada (SAS) para leer un blob privado en Azure.
    blob_name debe ser la ruta dentro del contenedor, ej:
    'certificados/reconocimientos/OIP_1.webp'
    """
    
    # 1. Validar si es una URL externa (http) para evitar procesarla
    if not blob_name or blob_name.startswith(("http://", "https://")):
        return blob_name or ""

    account_name = os.getenv("AZURE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_ACCOUNT_KEY")
    container_name = os.getenv("AZURE_CONTAINER")
    
    # 2. Corregir el error de 'None' como string en la conversión a int
    expiry_val = os.getenv("AZURE_URL_EXPIRATION_SECS")
    if expiry_val is None or expiry_val == "None" or expiry_val == "":
        expiry_seconds = 3600
    else:
        try:
            expiry_seconds = int(expiry_val)
        except ValueError:
            expiry_seconds = 3600

    if not account_name or not account_key or not container_name:
        # Si falta configuración, devolvemos el nombre original para no romper la vista
        return blob_name

    try:
        # Generar el token SAS
        sas = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            # Usamos datetime.now() para evitar problemas de compatibilidad en versiones nuevas
            expiry=datetime.utcnow() + timedelta(seconds=expiry_seconds),
        )

        return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas}"
    
    except Exception as e:
        # Si algo falla en la generación (ej. caracteres extraños), devolvemos el string original
        print(f"Error generando SAS para {blob_name}: {e}")
        return blob_name