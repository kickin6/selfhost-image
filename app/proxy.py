from flask import Flask, request, jsonify
from .utils import generate_random_filename
import requests
import logging
from .validations import is_valid_api_key, validate_api_key
from .config import Config

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

@app.route('/image/v1/authenticate')
@validate_api_key(pass_api_key=False)
def authenticate():
    return jsonify({'message': 'API key is valid'}), 200

@app.route('/image/v1/create-image', methods=['POST'])
@validate_api_key(pass_api_key=True)
def proxy(api_key):
    logger.info("Proxy route hit")
    data = request.json
    if data:
        logger.info(f"Received POST data: {data}")
    else:
        logger.info("No POST data received")

    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    logger.info(f"Sending headers: {headers}")

    # Forward the request to the Fooocus API
    try:
        data["save_name"] = f"{api_key}"
        response = requests.post(
            'http://fooocus:8888/v1/generation/text-to-image',
            json=data,
            headers=headers
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        logger.info(f"Response from Fooocus API: {response.json()}")
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        if e.response is not None:
            logger.error(f"Error forwarding request to Fooocus API: {e.response.status_code} {e.response.text}")
        else:
            logger.error(f"Error forwarding request to Fooocus API: {e}")
        return jsonify({"error": "Failed to forward request"}), 500

if __name__ == '__main__':
    logger.info("Starting Flask proxy")
    app.run(host='0.0.0.0', port=5000)

