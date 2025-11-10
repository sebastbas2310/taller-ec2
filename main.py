from fastapi import FastAPI
from models.person import Person
import boto3
import json
from datetime import datetime

app = FastAPI(title="API con FastAPI y S3")

# Configurar cliente S3
s3 = boto3.client('s3')
BUCKET_NAME = "tu-bucket-s3"

@app.post("/insert")
def insert_person(person: Person):
    """
    Recibe los datos validados de una persona,
    los guarda como JSON en S3
    y retorna el número total de archivos en el bucket.
    """
    # Crear nombre de archivo único
    filename = f"person_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Subir el archivo a S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=json.dumps(person.dict())
    )

    # Contar cuántos archivos hay actualmente en el bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    total_files = response.get('KeyCount', 0)

    # ✅ Retornar solo el número total de archivos (como pide el enunciado)
    return {"total_archivos_en_bucket": total_files}
