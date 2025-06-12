import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    bucket_name = os.environ["BUCKET_NAME"] 

    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)

    comentario_json = json.dumps(comentario)
    archivo_nombre = f"comentarios/{tenant_id}/{uuidv1}.json"
    s3 = boto3.client('s3')
        
    s3.put_object(
            Bucket=bucket_name,
            Key=archivo_nombre,
            Body=comentario_json,  
            ContentType='application/json'  
        )
        


    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response
    }
