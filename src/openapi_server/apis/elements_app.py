from typing import Dict, List 
import importlib
import pkgutil

from openapi_server.apis.elements_api_base import BaseElementsApi
import openapi_server.impl
from fastapi import (
    APIRouter, 
    Body,
    Cookie, 
    Form, 
    Header, 
    HTTPException, 
    Path, 
    Query, 
    Response, 
    Security, 
    status
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.element import Element
from openapi_server.models.element_short_list import ElementShortList
from openapi_server.models.get_element_header import GetElementHeader
from openapi_server.models.get_event_data import GetEventData
from openapi_server.models.get_measurement_pass_series import GetMeasurementPassSeries
from openapi_server.models.getdata_series import GetdataSeries
from openapi_server.security_api import get_token_bearer

router= APIRouter()
ns_pkg =openapi_server.impl
for _, name , _ in pkgutil.inter_models(ns_pkg.__path__, ns_pkg.__name__+"."):
    importlib.import_module(name)


@router.get(
    "/Fleet/Equipment/{oemISOidentifier}/elements/{element_uid}/data_series/",
    responses={
        200: {"model": GetdataSeries, "description": "Successful operation"},
        400: {"description": "Invalid parameter supplied"},
        404: {"description": "No element(s) found"},
    },
    tags=["Elements"],
    summary="Get selected data_series of element with uid",
    response_model_by_alias=True,
)

async def get_element_data_series(
    oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
    element_uid: str = Path(..., description="Unique Id of the element"),
    page_number: int = Query(None, description="Page number, starting from 1", alias="page-number"),
    token_bearer: TokenModel = Security(
        get_token_bearer
    ),
) -> GetdataSeries:
    """Returns requested dataseries from the list about one element"""
    if not BaseElementsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseElementsApi.subclasses[0]().get_element_data_series(oemISOidentifier, element_uid, page_number)

@router.get(
    "/Fleet/Equipment/{oemISOidentifier}/elements/{element_uid}",
    responses = {
        200:{"model":Element, "description": "Successful operation"}, 
        400 :{"description":"Invalid parameters supplied"}, 
        404 : {"description": "No elements  found"},
    }, 
    tags = ["Elemenst"], 
    summary= "Get all value of element with uid", 
    response_model_by_alias= True
)
    