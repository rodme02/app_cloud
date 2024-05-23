import boto3
from botocore.exceptions import ClientError
from flask import Flask, request, jsonify
import logging

# Inicializando o Flask
app = Flask(__name__)

# Inicializando o DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
table = dynamodb.Table('UsersTable')

# Configurando o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Função para lidar com exceções do DynamoDB
def handle_dynamodb_exception(e):
    logger.error(f"An error occurred: {e}")

    return jsonify({'error': str(e)}), 500

# Função para validar os dados do usuário
def validate_user_data(user_data, fields):
    missing_fields = [field for field in fields if field not in user_data]

    if missing_fields:
        return False, {'error': f"{', '.join(missing_fields)} are required fields"}, 400
    
    return True, None, None

# Rota para verificar a saúde da aplicação
@app.route('/health', methods=['GET'])
def health():
    healthy = {'DynamoDB': 'Healthy'}

    try:
        table.table_status

    except ClientError as e:
        healthy['DynamoDB'] = 'Unhealthy'
        return handle_dynamodb_exception(e)
    
    status = 'Healthy' if all(status == 'Healthy' for status in healthy.values()) else 'Unhealthy'

    return jsonify({'details': healthy}), 200 if status == 'Healthy' else 500

# Rota para adicionar um usuário
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        user_data = request.json

        valid, error_response, status_code = validate_user_data(user_data, ['id', 'name'])

        if not valid:
            return jsonify(error_response), status_code

        user_id = int(user_data['id'])

        if 'Item' in table.get_item(Key={'id': user_id}):
            return jsonify({'error': 'User already exists, use /update_user to update a user.'}), 400

        item = {'id': user_id, 'name': user_data['name']}

        response = table.put_item(Item=item)

        return jsonify({'message': 'User {} created successfully'.format(item), 'response': response}), 200
    
    except ClientError as e:
        return handle_dynamodb_exception(e)

# Rota para recuperar um usuário
@app.route('/get_user/<int:id>', methods=['GET'])
def get_user(id):
    try:
        response = table.get_item(Key={'id': id})

        item = response.get('Item')

        item['id'] = int(item['id'])

        if not item:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'message': 'User {} retrieved successfully'.format(item), 'response': response}), 200
    
    except ClientError as e:
        return handle_dynamodb_exception(e)

# Rota para atualizar um usuário
@app.route('/update_user', methods=['PUT'])
def update_user():
    try:
        user_data = request.json

        valid, error_response, status_code = validate_user_data(user_data, ['id'])

        if not valid:
            return jsonify(error_response), status_code

        item = {'id': int(user_data['id']), 'name': user_data.get('name')}

        response = table.put_item(Item=item)

        return jsonify({'message': 'User {} updated successfully'.format(item), 'response': response}), 200
    
    except ClientError as e:
        return handle_dynamodb_exception(e)

# Rota para deletar um usuário
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        item = table.get_item(Key={'id': id})

        item['id'] = int(item['id'])

        response = table.delete_item(Key={'id': id})

        return jsonify({'message': 'User {} deleted successfully'.format(item.get('Item')), 'response': response}), 200
    
    except ClientError as e:
        return handle_dynamodb_exception(e)

# Rodando a aplicação em HTTP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
