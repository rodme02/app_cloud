import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Inicializa o dynamodb
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
table = dynamodb.Table('MyDynamoDBTable2')

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

@app.route("/health", methods=["GET"])
def health_check():
    healthy = {"DynamoDB": "Healthy"}
    try:
        table.table_status
    except NoCredentialsError:
        logger.error("NoCredentialsError")
        healthy["DynamoDB"] = "NoCredentialsError"
    except PartialCredentialsError:
        logger.error("PartialCredentialsError")
        healthy["DynamoDB"] = "PartialCredentialsError"
    except Exception as e:
        logger.error(e)
        healthy["DynamoDB"] = "Unhealthy", str(e)

    status = "Healthy" if all(value == "Healthy" for value in healthy.values()) else "Unhealthy"

    return jsonify({"status": status, "dependencies": healthy}), 200 if status == "Healthy" else 500

@app.post("/users", methods=["POST"])
def create_user():
    user = request.json
    try:
        table.put_item(Item=user)
        
        if not user.get('id') or not user.get('name'):
            return jsonify({'error': 'Missing required fields id and name'}), 400
        
        new_user = {
            'id': user['id'],
            'name': user['name']
        }

        if 'id' in table.get_item(Key={'id': user['id']}).get('Item', {}):
            return jsonify({'error': 'User already exists'}), 400
        
        response = table.put_item(Item=new_user)

        return jsonify({'message': 'User created successfully', 'user': new_user}), 200
    
    except NoCredentialsError:
        logger.error("NoCredentialsError")
        return jsonify({'error': 'NoCredentialsError'}), 500
    except PartialCredentialsError:
        logger.error("PartialCredentialsError")
        return jsonify({'error': 'PartialCredentialsError'}), 500
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500

@app.get("/users", methods=["GET"])
def get_users():
    try:
        response = table.scan()
        return jsonify(response.get('Items', []))
    except NoCredentialsError:
        logger.error("NoCredentialsError")
        return jsonify({'error': 'NoCredentialsError'}), 500
    except PartialCredentialsError:
        logger.error("PartialCredentialsError")
        return jsonify({'error': 'PartialCredentialsError'}), 500
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500
         
@app.get("/users/<id>", methods=["GET"])
def get_user(id):
    try:
        response = table.get_item(Key={'id': id})
        return jsonify(response.get('Item', {}))
    
    except NoCredentialsError:
        logger.error("NoCredentialsError")
        return jsonify({'error': 'NoCredentialsError'}), 500
    except PartialCredentialsError:
        logger.error("PartialCredentialsError")
        return jsonify({'error': 'PartialCredentialsError'}), 500
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500
    
@app.delete("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        response = table.delete_item(Key={'id': id})
        return jsonify({'message': 'User deleted successfully', 'response': response}), 200
    
    except NoCredentialsError:
        logger.error("NoCredentialsError")
        return jsonify({'error': 'NoCredentialsError'}), 500
    except PartialCredentialsError:
        logger.error("PartialCredentialsError")
        return jsonify({'error': 'PartialCredentialsError'}), 500
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500
    
@app.put("/users/<id>", methods=["PUT"])
def update_user(id):
    user = request.json
    try:
        if not user.get('name'):
            return jsonify({'error': 'Missing required field name'}), 400
        
        new_user = {
            'id': id,
            'name': user['name']
        }
        
        response = table.put_item(Item=new_user)
        
        return jsonify({'message': 'User updated successfully', 'user': new_user, 'response': response}), 200
    
    except NoCredentialsError:
        logger.error("NoCredentialsError")
        return jsonify({'error': 'NoCredentialsError'}), 500
    except PartialCredentialsError:
        logger.error("PartialCredentialsError")
        return jsonify({'error': 'PartialCredentialsError'}), 500
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    # Executa a aplicação em HTTP
    app.run(host='0.0.0.0', port=80)