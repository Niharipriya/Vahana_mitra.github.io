import re
from typing import Any


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _extract_location_pair(text: str) -> dict[str, str]:
    """
    Very simple extractor for MVP.
    Example:
    'I need a truck from Hyderabad to Vijayawada'
    """
    match = re.search(r"from\s+(.+?)\s+to\s+(.+)", text, re.IGNORECASE)
    if not match:
        return {}

    return {
        "pickup_location": match.group(1).strip(),
        "drop_location": match.group(2).strip(),
    }


def generate_chatbot_reply(message: str, session_data: Any, user=None) -> dict:
    text = _normalize(message)

    # Greeting
    if _contains_any(text, ["hi", "hello", "hey"]):
        return {
            "reply": (
                "Hello! I can help you book a lorry, find a load for your truck, "
                "explain registration, or guide you to the right page."
            ),
            "action": None
        }

    # Truck booking intent
    if _contains_any(text, [
        "book a lorry", "book truck", "need a truck", "need lorry", "find truck"
    ]):
        extracted = _extract_location_pair(message)
        if extracted:
            session_data["chat_prefill"] = {
                "flow": "load",
                **extracted
            }
            return {
                "reply": (
                    f"I understood that you want a truck from "
                    f"{extracted['pickup_location']} to {extracted['drop_location']}. "
                    "I can take you to the load registration flow."
                ),
                "action": {
                    "type": "redirect",
                    "url": "/register/load"
                }
            }

        return {
            "reply": (
                "Sure. To book a lorry, I need at least pickup location, drop location, "
                "vehicle type, and estimated load weight. You can start from the truck booking form."
            ),
            "action": {
                "type": "redirect",
                "url": "/"
            }
        }

    # Load finding intent
    if _contains_any(text, [
        "empty truck", "find load", "i have truck", "available truck", "need material"
    ]):
        return {
            "reply": (
                "Got it. You want to find a load for your truck. "
                "You can continue through truck registration and mention current location, "
                "vehicle type, capacity, and destination preference."
            ),
            "action": {
                "type": "redirect",
                "url": "/register/truck"
            }
        }

    # Signup/login help
    if _contains_any(text, ["sign up", "signup", "register account", "create account"]):
        return {
            "reply": "You can create your account from the signup page.",
            "action": {
                "type": "redirect",
                "url": "/auth/signup"
            }
        }

    if _contains_any(text, ["login", "log in", "sign in"]):
        return {
            "reply": "You can log in from the login page.",
            "action": {
                "type": "redirect",
                "url": "/auth/login"
            }
        }

    # FAQ-like responses
    if _contains_any(text, ["what details", "required details", "what do i need"]):
        return {
            "reply": (
                "For booking a truck, usually you need pickup location, drop location, "
                "load weight, and preferred vehicle type. "
                "For truck availability, you need current location, truck type, and capacity."
            ),
            "action": None
        }

    return {
        "reply": (
            "I can help with booking a truck, finding a load, login/signup guidance, "
            "and explaining what details are needed. Try saying: "
            "'I need a truck from Hyderabad to Vijayawada'."
        ),
        "action": None
    }