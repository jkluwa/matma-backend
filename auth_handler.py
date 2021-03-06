import time
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = 'deff1952d59f883eceq9j8abtm9fed21ab0ad9a53323eca4f'
JWT_ALGORITHM = 'HS256'


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user: str) -> Dict[str, str]:
    payload = {
        "user": user,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
