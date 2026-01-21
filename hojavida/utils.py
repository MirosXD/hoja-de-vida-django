from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
import os


def generar_sas_blob(blob_name: str) -> str:
    """
    Devuelve una URL firmada (SAS) para leer un blob privado en Azure.
    blob_name debe ser la ruta dentro del contenedor, ej:
    'certificados/reconocimientos/OIP_1.webp'
    """
    account_name = os.getenv("AZURE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_ACCOUNT_KEY")
    container_name = os.getenv("AZURE_CONTAINER")
    expiry_seconds = int(os.getenv("AZURE_URL_EXPIRATION_SECS", "3600"))

    if not account_name or not account_key or not container_name:
        # Si falta algo en el .env, devolvemos vacío y no rompe la vista
        return ""

    sas = generate_blob_sas(
        account_name=account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(seconds=expiry_seconds),
    )

    return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas}"
