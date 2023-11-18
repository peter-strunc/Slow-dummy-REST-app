import os
import time
import random
import logging
import uuid
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# In-memory database
users = {}

# Random delay logic with logging
def random_delay():
    average_wait = float(os.getenv('AVERAGE_WAIT_MS', 1000)) / 1000  # Default is 1000 ms converted to seconds
    deviation = average_wait * 0.2  # 20%
    time_to_wait = random.uniform(average_wait - deviation, average_wait + deviation)
    logging.info(f"Waiting for {time_to_wait:.3f} seconds.")
    time.sleep(time_to_wait)

@app.before_request
def before_request():
    """Add a random delay before each request with logging."""
    random_delay()

# Get user by ID
@app.route('/user/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    else:
        abort(404)

# Create a new user
@app.route('/user', methods=['POST'])
def create_user():
    # Log the entire JSON payload
    logging.info(f"Incoming JSON data: {request.json}")

    if not request.json:
        logging.error("No JSON data in request")
        abort(400)
    
    if 'username' not in request.json:
        logging.error("No 'username' in JSON data")
        abort(400)
    
    if 'id' not in request.json:
        logging.error("No 'id' in JSON data")
        abort(400)
    
    user_id = request.json['id']
    if not isinstance(user_id, str):
        logging.error(f"'id' is not a string: {user_id}")
        abort(400)
    
    user = request.json
    users[user_id] = user
    return jsonify(user), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
