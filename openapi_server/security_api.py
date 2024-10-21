# coding: utf-8

from typing import List


from fastapi import Depends, Security  # noqa: F401
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows  # noqa: F401
from fastapi.security import (  # noqa: F401
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    OAuth2,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi.security.api_key import APIKeyCookie, APIKeyHeader, APIKeyQuery  # noqa: F401

from openapi_server.models.extra_models import TokenModel
import jwt
from jose import jwt, JWTError, ExpiredSignatureError
import base64
import json
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
bearer_auth = HTTPBearer()


def base64_url_decode(input_str):
    # Make input length a multiple of 4 to avoid padding errors
    padded = input_str + '==' 
    return base64.urlsafe_b64decode(padded)

def get_token_bearer(credentials: HTTPAuthorizationCredentials = Depends(bearer_auth)):
    """
    Check and retrieve authentication information from custom bearer token.

    :param credentials: Credentials provided by Authorization header
    :type credentials: HTTPAuthorizationCredentials
    :return: Decoded token information or None if token is invalid
    :rtype: dict | None
    """
    token = credentials.credentials
    try:
        header, payload, signature = token.split('.')
        decoded_bytes = base64_url_decode(payload)
        decoded_token = json.loads(decoded_bytes.decode('utf-8'))

    except (ValueError, json.JSONDecodeError):
        raise HTTPException(status_code=401, detail="Invalid token")

    tenant_admin = "TENANT_ADMIN" in decoded_token.get("scopes", [])
    customer_id = decoded_token.get("customerId", None)
    user_id = decoded_token.get("userId", None)
    first_name = decoded_token.get("firstName", "")
    last_name = decoded_token.get("lastName", "")

    return {
        "token": token,
        "tenant_admin": tenant_admin,
        "customer_id": customer_id,
        "user_id": user_id,
        "name": f"{first_name} {last_name}"
    }

