import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Initialize DynamoDB's boto3 client
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
table = dynamodb.Table('UsersTable')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


@app.route('/health', methods=['GET'])
def health():
    healthy = {'DynamoDB': 'Healthy'}
    try:
        # Check if DynamoDB table is available
        table.table_status
    except NoCredentialsError:
        logger.error("Credentials not available")
        healthy['DynamoDB'] = 'Degraded - No credentials'
    except PartialCredentialsError:
        logger.error("Incomplete credentials")
        healthy['DynamoDB'] = 'Degraded - Incomplete credentials'
    except Exception as e:
        logger.error(f"An error occurred with DynamoDB: {e}")
        healthy['DynamoDB'] = f'Unhealthy - {e}'
    
    status = 'Healthy' if all(status == 'Healthy' for status in healthy.values()) else 'Unhealthy'
    
    return jsonify({'message': status, 'details': healthy}), 200 if status == 'Healthy' else 500

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        # Get data from the request
        user_data = request.json
        
        # Validate input
        if not user_data.get('id') or not user_data.get('name'):
            return jsonify({'error': 'id and name are required fields'}), 400
        
        # Ensure id is included in the item
        item = {
            'id': user_data['id'],
            'name': user_data['name'],
        }
        
        if 'id' in table.get_item(Key={'id': user_data['id']}).get('Item', {}):
            return jsonify({'error': 'User already exists, post to /update_user to update an user.'}), 400
        # Save data to DynamoDB
        response = table.put_item(Item=item)
        
        return jsonify({'message': 'User added successfully', 'response': response}), 200
    except NoCredentialsError:
        logger.error("Credentials not available")
        return jsonify({'error': 'Credentials not available'}), 500
    except PartialCredentialsError:
        logger.error("Incomplete credentials")
        return jsonify({'error': 'Incomplete credentials'}), 500
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_user', methods=['GET'])
def get_user():
    try:
        # Get id from the request
        id = request.args.get('id')
        
        # Validate input
        if not id:
            return jsonify({'error': 'id is a required field'}), 400
        
        # Get user data from DynamoDB
        response = table.get_item(Key={'id': id})
        
        return jsonify({'message': 'User retrieved successfully', 'user_data': response.get('Item', {})})
    except NoCredentialsError:
        logger.error("Credentials not available")
        return jsonify({'error': 'Credentials not available'}), 500
    except PartialCredentialsError:
        logger.error("Incomplete credentials")
        return jsonify({'error': 'Incomplete credentials'}), 500
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/update_user', methods=['PUT'])
def update_user():
    try:
        # Get data from the request
        user_data = request.json
        
        # Validate input
        if not user_data.get('id'):
            return jsonify({'error': 'id is a required field'}), 400
        
        # Ensure id is included in the item
        item = {
            'id': user_data['id'],
            'name': user_data.get('name'),
            # Include other attributes as necessary
        }
        
        # Save data to DynamoDB
        response = table.put_item(Item=item)
        
        return jsonify({'message': 'User updated successfully', 'response': response}), 200
    except NoCredentialsError:
        logger.error("Credentials not available")
        return jsonify({'error': 'Credentials not available'}), 500
    except PartialCredentialsError:
        logger.error("Incomplete credentials")
        return jsonify({'error': 'Incomplete credentials'}), 500
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    try:
        # Get id from the request
        id = request.args.get('id')
        
        # Validate input
        if not id:
            return jsonify({'error': 'id is a required field'}), 400
        
        # Delete user data from DynamoDB
        response = table.delete_item(Key={'id': id})
        
        return jsonify({'message': 'User deleted successfully', 'response': response}), 200
    except NoCredentialsError:
        logger.error("Credentials not available")
        return jsonify({'error': 'Credentials not available'}), 500
    except PartialCredentialsError:
        logger.error("Incomplete credentials")
        return jsonify({'error': 'Incomplete credentials'}), 500
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)