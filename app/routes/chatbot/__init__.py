from flask import Blueprint, request, jsonify, session, url_for
from flask_login import current_user

from app.services.chatbot_service import generate_chatbot_reply

bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")


@bp.route("/message", methods=["POST"])
def message():
    payload = request.get_json(silent=True) or {}
    user_message = (payload.get("message") or "").strip()

    if not user_message:
        return jsonify({
            "reply": "Please type a message.",
            "action": None
        }), 400

    response = generate_chatbot_reply(
        message=user_message,
        session_data=session,
        user=current_user if current_user.is_authenticated else None
    )

    return jsonify(response), 200