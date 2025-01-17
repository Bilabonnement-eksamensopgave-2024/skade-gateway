from flask import Flask, jsonify, request
import requests
import os
from flasgger import swag_from
from dotenv import load_dotenv
from swagger.config import init_swagger

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# MICROSERVICES:
MICROSERVICES = {
    "subscription": os.getenv("ABONNEMENT_MICROSERVICE_URL", "http://localhost:5002"),
    "car": os.getenv("CAR_MICROSERVICE_URL", "http://localhost:5004"),
    "user": os.getenv("LOGIN_MICROSERVICE_URL", "http://localhost:5005")
}

# Initialize Swagger
init_swagger(app)

# ----------------------------------------------------- Root Endpoint: GET /
@app.route('/', methods=['GET'])
def service_info():
    return jsonify({
        "service": "Sales Gateway",
        "description": "This gateway manages sales operations including subscriptions, pricing, and inventory.",
        "endpoints": [
            {
                "path": "/subscriptions",
                "method": "GET",
                "description": "Get all subscriptions",
                "response": "JSON array of subscription objects",
                "role_required": "admin, sales"
            },
            {
                "path": "/subscriptions/<int:id>",
                "method": "GET",
                "description": "Get subscription by ID",
                "response": "JSON object of the subscription",
                "role_required": "admin, sales"
            },
            {
                "path": "/subscriptions/<int:id>/car",
                "method": "GET",
                "description": "Get car information for a subscription",
                "response": "JSON object of the car information",
                "role_required": "admin, sales"
            },
            {
                "path": "/subscriptions",
                "method": "POST",
                "description": "Create a new subscription",
                "response": "JSON object of the created subscription",
                "role_required": "admin, sales"
            },
            {
                "path": "/subscriptions/<int:id>",
                "method": "PATCH",
                "description": "Update subscription by ID",
                "response": "JSON object of the updated subscription",
                "role_required": "admin, sales"
            },
            {
                "path": "/cars/available",
                "method": "GET",
                "description": "Get all available cars",
                "response": "JSON array of available car objects",
                "role_required": "admin, sales"
            },
            {
                "path": "/subscriptions/<int:id>",
                "method": "DELETE",
                "description": "Delete subscription by ID",
                "response": "JSON object of the deleted subscription",
                "role_required": "admin, sales"
            },
            {
                "path": "/login",
                "method": "POST",
                "description": "User login",
                "response": "JSON object with login details and authorization token",
                "role_required": "none"
            },
            {
                "path": "/health",
                "method": "GET",
                "description": "Health check",
                "response": "JSON object with status of the service",
                "role_required": "none"
            }
        ]
    }), 200

# ----------------------------------------------------- GET /subscriptions
@app.route('/subscriptions', methods=['GET'])
@swag_from('swagger/get_subscriptions.yaml')
def get_subscriptions():
    try:
        response = requests.get(f"{MICROSERVICES['subscription']}/subscriptions",cookies=request.cookies)
        response.raise_for_status()
        try: 
            data = response.json() 
        except requests.exceptions.JSONDecodeError: 
            data = []
        return jsonify(data), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch from microservice", "details": str(e)}), 500

# ----------------------------------------------------- GET /subscriptions/id
@app.route('/subscriptions/<int:id>', methods=['GET'])
@swag_from('swagger/get_subscription_by_id.yaml')
def get_subscription(id):
    try:
        response = requests.get(f"{MICROSERVICES['subscription']}/subscriptions/{id}",cookies=request.cookies)
        response.raise_for_status()
        try: 
            data = response.json() 
        except requests.exceptions.JSONDecodeError: 
            data = []
        return jsonify(data), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch from microservice", "details": str(e)}), 500

# ----------------------------------------------------- GET /subscriptions/id/car
@app.route('/subscriptions/<int:id>/car', methods=['GET'])
@swag_from('swagger/get_subscription_car_info.yaml')
def get_subscription_car_info(id):
    try:
        response = requests.get(f"{MICROSERVICES['subscription']}/subscriptions/{id}/car",cookies=request.cookies)
        response.raise_for_status()
        try: 
            data = response.json() 
        except requests.exceptions.JSONDecodeError: 
            data = []
        return jsonify(data), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch from microservice", "details": str(e)}), 500

# ----------------------------------------------------- POST /subscriptions
@app.route('/subscriptions', methods=['POST'])
@swag_from('swagger/post_subscriptions.yaml')
def post_subscription():
    try:
        response = requests.post(
            f"{MICROSERVICES['subscription']}/subscriptions",
            json=request.json,
            cookies=request.cookies
        )
        response.raise_for_status()
        try: 
            data = response.json() 
        except requests.exceptions.JSONDecodeError: 
            data = []
        return jsonify(data), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch from microservice", "details": str(e)}), 500

# ----------------------------------------------------- PATCH /subscriptions/id
@app.route('/subscriptions/<int:id>', methods=['PATCH'])
@swag_from('swagger/patch_subscription.yaml')
def patch_subscription(id):
    try:
        response = requests.patch(
            f"{MICROSERVICES['subscription']}/subscriptions/{id}",
            json=request.json,
            cookies=request.cookies
        )
        response.raise_for_status()
        try: 
            data = response.json() 
        except requests.exceptions.JSONDecodeError: 
            data = []
        return jsonify(data), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch from microservice", "details": str(e)}), 500

# ----------------------------------------------------- GET /cars/available
@app.route('/cars/available', methods=['GET'])
@swag_from('swagger/get_available_cars.yaml')
def get_cars():
    try:
        response = requests.get(f"{MICROSERVICES['car']}/cars/available",cookies=request.cookies)
        response.raise_for_status()
        try: 
            data = response.json() 
        except requests.exceptions.JSONDecodeError: 
            data = []
        return jsonify(data), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch from microservice", "details": str(e)}), 500

# ----------------------------------------------------- DELETE /subscriptions/id
@app.route('/subscriptions/<int:id>', methods=['DELETE'])
@swag_from('swagger/delete_subscription.yaml')
def delete_subscription(id):
    try:
        response = requests.delete(f"{MICROSERVICES['subscription']}/subscriptions/{id}",cookies=request.cookies)
        response.raise_for_status()
        try: 
            data = response.json() 
        except requests.exceptions.JSONDecodeError: 
            data = []
        return jsonify(data), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch from microservice", "details": str(e)}), 500

# ----------------------------------------------------- POST /login
@app.route('/login', methods=['POST'])
def login():
    response = requests.post(
        url=f"{MICROSERVICES['user']}/login",
        cookies=request.cookies,
        json=request.json,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        response_data = response.json()
        
        # Create the Flask response
        flask_response = jsonify(response_data)
        
        # Extract cookies from the microservice response
        if 'Authorization' in response.cookies:
            auth_cookie = response.cookies['Authorization']
            flask_response.set_cookie('Authorization', auth_cookie, httponly=True, secure=True)
        
        return flask_response, 200
    else:
        data = response.json()
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /health
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# ----------------------------------------------------- Catch-all route for unmatched endpoints
@app.errorhandler(404)
def page_not_found_404(e):
    return jsonify({"message": "Endpoint does not exist"}), 404

@app.errorhandler(405)
def page_not_found_405(e):
    return jsonify({"message": "Method not allowed - double-check the method you are using"}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)), debug=True)
