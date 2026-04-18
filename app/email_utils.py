"""
Email utilities for Vahana Mitra.

HOW TOKENS WORK:
  When a user signs up, we generate a unique token tied to their email.
  The token is a scrambled string like: eyJhbGciOiJIUzI1NiJ9...
  We send it as a link: /auth/verify/<token>
  When clicked, we decode the token to get the email back.
  If the token is valid and not expired (24hrs), we mark the account verified.

WHY itsdangerous?
  It uses your app's SECRET_KEY to sign the token — so nobody can
  forge a fake token to verify someone else's account.
"""

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app, url_for
from flask_mail import Message
from app import mail


def generate_verification_token(email: str) -> str:
    """
    Takes an email address and returns a secure token.
    Example: "user@gmail.com" → "eyJhbGci..."
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verification')


def verify_token(token: str, max_age_seconds: int = 3600):
    """
    Takes a token and decodes it back to an email.
    max_age_seconds=86400 means the token expires after one hours.
    Returns the email if valid, or None if expired/invalid.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-verification', max_age=max_age_seconds)
        return email
    except SignatureExpired:
        return None  # Token expired
    except BadSignature:
        return None  # Token was tampered with


def send_verification_email(user_email: str):
    """
    Sends a verification email to the user.
    The link contains their unique token.
    """
    token = generate_verification_token(user_email)

    # url_for builds the full URL: https://yourdomain.com/auth/verify/<token>
    verify_url = url_for('auth.verify_email', token=token, _external=True)

    msg = Message(
        subject="Verify your Vahana Mitra account (valid for one hour from when it is generated)",
        recipients=[user_email]
    )

    msg.html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: auto; padding: 20px;">
        <h2 style="color: #2c3e50;">Welcome to Vahana Mitra!</h2>
        <p>Thank you for signing up. Please verify your email address by clicking the button below.</p>
        <a href="{verify_url}"
           style="display: inline-block; padding: 12px 24px; background-color: #2c3e50;
                  color: white; text-decoration: none; border-radius: 6px; margin: 16px 0;">
            Verify My Email
        </a>
        <p style="color: #888; font-size: 13px;">This link expires in 24 hours.</p>
        <p style="color: #888; font-size: 13px;">If you didn't create this account, ignore this email.</p>
    </div>
    """

    mail.send(msg)
