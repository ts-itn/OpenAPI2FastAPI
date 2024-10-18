# File: openapi_server/impl/__init__.py

from typing import Tuple, Type
from openapi_server.apis.elements_api_base import BaseElementsApi
from openapi_server.impl.elements_api_client import ElementsApiClient  # Import your subclass

# Manually register the subclass
BaseElementsApi.subclasses = (ElementsApiClient,)
