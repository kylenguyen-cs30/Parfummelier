from flask import Blueprint, jsonify
from flask_cors import cross_origin

test_bp = Blueprint("test", __name__)


@test_bp.route("/cors-test", methods=["GET"])
@cross_origin(origins=["http://forum-service:5000"])
def test_cors():
    return jsonify(
        {
            "status": "success",
            "message": "CORS test successful",
            "service": "user-service",
        }
    )
