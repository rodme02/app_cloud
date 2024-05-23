import subprocess
import requests
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def dns_finder():
    try:
        # Run the bash script to get the DNS
        result = subprocess.run(['bash', 'dns_finder.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            logger.error(f"Error getting DNS: {result.stderr}")
            return None
        
        dns = result.stdout.strip()
        logger.info(f"Retrieved DNS: {dns}")
        return dns
    except Exception as e:
        logger.error(f"An error occurred while getting DNS: {e}")
        return None

def check_health(dns):
    try:
        url = f"http://{dns}/health"
        response = requests.get(url)
        
        if response.status_code == 200:
            health_status = response.json()
            logger.info(f"Health check successful: {health_status}")
            return health_status
        else:
            logger.error(f"Health check failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        logger.error(f"An error occurred while checking health: {e}")
        return None

def add_user(dns, user_data):
    try:
        url = f"http://{dns}/add_user"
        response = requests.post(url, json=user_data)
        
        if response.status_code == 200:
            logger.info(f"User {user_data['user_id']} added successfully")
            return True
        else:
            logger.error(f"Add user {user_data['user_id']} failed with status code {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"An error occurred while adding user {user_data['user_id']}: {e}")
        return False

def get_user(dns, user_id):
    try:
        url = f"http://{dns}/get_user?user_id={user_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            user_data = response.json().get('user_data', {})
            logger.info(f"User {user_id} retrieved successfully: {user_data}")
            return user_data
        else:
            logger.error(f"Get user {user_id} failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        logger.error(f"An error occurred while getting user {user_id}: {e}")
        return None

def update_user(dns, user_data):
    try:
        url = f"http://{dns}/update_user"
        response = requests.put(url, json=user_data)
        
        if response.status_code == 200:
            logger.info(f"User {user_data['user_id']} updated successfully")
            return True
        else:
            logger.error(f"Update user {user_data['user_id']} failed with status code {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"An error occurred while updating user {user_data['user_id']}: {e}")
        return False

def delete_user(dns, user_id):
    try:
        url = f"http://{dns}/delete_user?user_id={user_id}"
        response = requests.delete(url)
        
        if response.status_code == 200:
            logger.info(f"User {user_id} deleted successfully")
            return True
        else:
            logger.error(f"Delete user {user_id} failed with status code {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"An error occurred while deleting user {user_id}: {e}")
        return False

def main():
    dns = dns_finder()
    if dns:
        health_status = check_health(dns)
        if health_status and health_status['message'] == 'Healthy':
            users = [
                {'user_id': 'user1', 'name': 'Test User 1'},
                {'user_id': 'user2', 'name': 'Test User 2'},
                {'user_id': 'user3', 'name': 'Test User 3'},
                {'user_id': 'mat', 'name': 'matt'}
            ]

            for user in users:
                if add_user(dns, user):
                    retrieved_user = get_user(dns, user['user_id'])
                    if retrieved_user:
                        updated_user_data = {'user_id': user['user_id'], 'name': f"Updated {user['name']}"}
                        if update_user(dns, updated_user_data):
                            if not delete_user(dns, user['user_id']):
                                logger.error(f"Failed to delete user {user['user_id']}")
                        else:
                            logger.error(f"Failed to update user {user['user_id']}")
                    else:
                        logger.error(f"Failed to retrieve user {user['user_id']}")
                else:
                    logger.error(f"Failed to add user {user['user_id']}")
        else:
            logger.error("Health check failed or DynamoDB is not healthy")
    else:
        logger.error("Failed to retrieve DNS")

if __name__ == "__main__":
    main()