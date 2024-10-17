from typing  import List 
from fastapi import  Depends, Security
from fastapi.openapi.model import OAuthiFlowImplicit, OAthFlows
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic, 
    HTTPBasicCredentials, 
    HTTPBearer, 
    OAuth2, 
    OAuth2PasswordBearer,
    Outh2AuthorizationCodeBearer, 
    SecurityScopes
), 
from fastapi.security.api_key import APIKeyCookie , APIKeyHeader , APIKeyQuery
from openapi_server.models.extra_models import TokenModel

bearer_auth = HTTPBearer()
def get_toke_bearer(credentials:HTTPAuthorizationCredentials= Depends(bearer_auth))-> TokenModel:
    