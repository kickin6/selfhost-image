import re
import os
from urllib.parse import urlparse

from functools import wraps
from flask import request, jsonify, current_app
from jsonschema import validate, ValidationError

from .config import Config
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def directory_exists(api_key):
    """Check if a directory exists for the given API key."""
    fullpath = os.path.normpath(os.path.join('/app/outputs', api_key))
    logger.debug("Checking if directory exists: %s", fullpath)
    if not fullpath.startswith('/app/outputs'):
        raise Exception("not allowed")
    
    # Add detailed logging for debugging
    directory_exists = os.path.isdir(fullpath)
    logger.debug("Directory exists: %s", directory_exists)
    
    # Log directory contents and permissions
    if directory_exists:
        logger.debug("Contents of /app/outputs: %s", os.listdir('/app/outputs'))
        logger.debug("Contents of %s: %s", fullpath, os.listdir(fullpath))
        logger.debug("Permissions of /app/outputs: %s", oct(os.stat('/app/outputs').st_mode))
        logger.debug("Permissions of %s: %s", fullpath, oct(os.stat(fullpath).st_mode))
    
    return directory_exists

def get_api_key():
    return request.headers.get('x-api-key')

def validate_api_key_logic(api_key):
    logger.debug("Validating API key: %s", api_key)
    if not api_key:
        return jsonify({'error': 'Missing x-api-key header'}), 400

    if not is_valid_api_key(api_key):
        return jsonify({'error': 'Invalid API key'}), 400

    if not directory_exists(api_key):
        return jsonify({'error': 'Directory does not exist'}), 400

    return None

def validate_api_key(pass_api_key=False):
    """Decorator to validate the API key."""
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            current_app.logger.debug("In validate_api_key decorator")
            api_key = get_api_key()
            if not api_key:
                current_app.logger.debug("Missing API key")
                return jsonify({'error': 'Missing x-api-key header'}), 400
            current_app.logger.debug(f"API key: {api_key}")
            if not is_valid_api_key(api_key):
                current_app.logger.debug("Invalid API key")
                return jsonify({'error': 'Invalid API key'}), 400
            if not directory_exists(api_key):
                current_app.logger.debug("Directory does not exist")
                return jsonify({'error': 'Directory does not exist'}), 400
            if pass_api_key:
                return func(*args, api_key=api_key, **kwargs)
            else:
                return func(*args, **kwargs)
        return decorated_function
    return decorator

def is_valid_api_key(api_key):
    return re.match(r'^[a-zA-Z0-9]+$', api_key) is not None

