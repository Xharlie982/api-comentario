import boto3
import uuid
import os
import json # <--- Importar json

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    
    # --- INICIO DE LA MODIFICACIÓN ---
    # Obtener nombres de la variables de entorno
    nombre_tabla = os.environ["TABLE_NAME"]
    nombre_bucket = os.environ["BUCKET_NAME"]
    # --- FIN DE LA MODIFICACIÓN ---

    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    
    # --- INICIO DE LA MODIFICACIÓN ---
    # Grabar en S3 (Estrategia Push) [cite: 183, 185]
    try:
        s3 = boto3.client('s3')
        # Crear un nombre de archivo único para el objeto S3
        s3_key = f"{uuidv1}.json"
        
        s3.put_object(
            Bucket=nombre_bucket,
            Key=s3_key,
            Body=json.dumps(comentario, indent=2) # Convertir el dict de Python a string JSON
        )
        print(f"Comentario guardado en S3: {nombre_bucket}/{s3_key}")
        
    except Exception as e:
        print(f"Error al guardar en S3: {e}")
        # (Opcional: puedes decidir si fallar la función aquí o solo registrar el error)
    # --- FIN DE LA MODIFICACIÓN ---

    # Grabar en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)
    
    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response
    }
