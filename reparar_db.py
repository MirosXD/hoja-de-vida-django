import sqlite3
import os

# Nombre de tu base de datos
db_path = 'db.sqlite3'

if not os.path.exists(db_path):
    print(f"❌ No se encontró el archivo {db_path} en esta carpeta.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Lista de comandos para añadir las columnas que faltan
    comandos = [
        'ALTER TABLE productosacademicos ADD COLUMN foto_producto VARCHAR(100);',
        'ALTER TABLE productoslaborales ADD COLUMN foto_producto VARCHAR(100);',
        'ALTER TABLE ventagarage ADD COLUMN foto VARCHAR(100);'
    ]
    
    print("Iniciando reparación...")
    for cmd in comandos:
        try:
            cursor.execute(cmd)
            print(f"✅ Ejecutado con éxito: {cmd[:40]}...")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"ℹ️ La columna ya existía, saltando...")
            else:
                print(f"❌ Error: {e}")

    conn.commit()
    conn.close()
    print("\n🚀 Proceso terminado. Ya puedes borrar este archivo y reiniciar el server.")