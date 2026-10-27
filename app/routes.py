import html

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.auth import verify_password, generate_token
from app.database import (
    get_user_by_username,
    get_notes,
    create_note,
)
BEARER_SCHEME = "Bearer"

api = Blueprint("api", __name__)


@api.post("/auth/login")
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Invalid credentials format"}), 400

    user = get_user_by_username(username)

    if user is None:
        return jsonify({"error": "Invalid credentials"}), 401

    if not verify_password(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user["id"])

    return jsonify({
        "access_token": token,
        "token_type": BEARER_SCHEME
    }), 200


@api.get("/api/data")
@jwt_required()
def get_data():
    user_id = int(get_jwt_identity())

    notes = get_notes(user_id)

    safe_notes = [
        {
            "id": note["id"],
            "title": html.escape(note["title"]),
            "content": html.escape(note["content"])
        }
        for note in notes
    ]

    return jsonify({"notes": safe_notes}), 200


@api.post("/api/data")
@jwt_required()
def add_data():
    user_id = int(get_jwt_identity())

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    title = data.get("title")
    content = data.get("content")

    if not isinstance(title, str) or not isinstance(content, str):
        return jsonify({"error": "Title and content must be strings"}), 400

    title = title.strip()
    content = content.strip()

    if not title or not content:
        return jsonify({"error": "Fields cannot be empty"}), 400

    if len(title) > 200 or len(content) > 5000:
        return jsonify({"error": "Input too long"}), 400

    note_id = create_note(user_id, title, content)

    return jsonify({
        "id": note_id,
        "title": html.escape(title),
        "content": html.escape(content)
    }), 201