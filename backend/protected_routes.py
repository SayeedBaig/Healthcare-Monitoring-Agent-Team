from flask import Flask, request, jsonify
from auth.jwt_handler import decode_access_token

app = Flask(__name__)

def token_required(f):
    def wrapper(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split()
            if len(parts) == 2 and parts[0].lower() == "bearer": token = parts[1]
        if not token: return jsonify({"error": "Token missing"}), 401
        try:
            decoded = decode_access_token(token)
            request.user = decoded
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/healthdata", methods=["GET"])
@token_required
def get_health_data():
    dummy_data = {
        "heart_rate": 72,
        "steps": 8421,
        "calories": 525,
        "message": f"Welcome {request.user.get('email', 'User')}, you accessed protected data!"
    }
    return jsonify(dummy_data), 200

if __name__ == "__main__": app.run(debug=True)