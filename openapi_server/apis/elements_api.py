# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.elements_api_base import BaseElementsApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.element import Element
from openapi_server.models.element_short_list import ElementShortList
from openapi_server.models.get_element_header import GetElementHeader
from openapi_server.models.get_event_data import GetEventData
from openapi_server.models.get_measurement_pass_series import GetMeasurementPassSeries
from openapi_server.models.getdata_series import GetdataSeries
from openapi_server.security_api import get_token_bearer

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
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
    responses={
        200: {"model": Element, "description": "Successful operation"},
        400: {"description": "Invalid parameter supplied"},
        404: {"description": "No element(s) found"},
    },
    tags=["Elements"],
    summary="Get all values of element with uid",
    response_model_by_alias=True,
)
async def get_element_details(
    oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
    element_uid: str = Path(..., description="unique Id of the element"),
    page_number: int = Query(None, description="Page number, starting from 1", alias="page-number"),
    token_bearer: TokenModel = Security(
        get_token_bearer
    ),
) -> Element:
    """Returns all information about one element"""
    if not BaseElementsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseElementsApi.subclasses[0]().get_element_details(oemISOidentifier, element_uid, page_number)


@router.get(
    "/Fleet/Equipment/{oemISOidentifier}/elements/{element_uid}/event_data/",
    responses={
        200: {"model": GetEventData, "description": "Successful operation"},
        400: {"description": "Invalid parameter supplied"},
        404: {"description": "No element(s) found"},
    },
    tags=["Elements"],
    summary="Get all event data of element with uid",
    response_model_by_alias=True,
)
async def get_element_event_data(
    oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
    element_uid: str = Path(..., description="unique Id of the element"),
    page_number: int = Query(None, description="Page number, starting from 1", alias="page-number"),
    token_bearer: TokenModel = Security(
        get_token_bearer
    ),
) -> GetEventData:
    """Returns requested event data about one element"""
    if not BaseElementsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseElementsApi.subclasses[0]().get_element_event_data(oemISOidentifier, element_uid, page_number)


@router.get(
    "/Fleet/Equipment/{oemISOidentifier}/elements/{element_uid}/measurement_pass/",
    responses={
        200: {"model": GetMeasurementPassSeries, "description": "Successful operation"},
        400: {"description": "Invalid parameter supplied"},
        404: {"description": "No element(s) found"},
    },
    tags=["Elements"],
    summary="Get all data_series of a measurement pass of element with uid",
    response_model_by_alias=True,
)
async def get_element_meassurement_data_series(
    oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
    element_uid: str = Path(..., description="unique Id of the element"),
    page_number: int = Query(None, description="Page number, starting from 1", alias="page-number"),
    token_bearer: TokenModel = Security(
        get_token_bearer
    ),
) -> GetMeasurementPassSeries:
    """Returns requested measurement pass dataseries about one element"""
    if not BaseElementsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseElementsApi.subclasses[0]().get_element_meassurement_data_series(oemISOidentifier, element_uid, page_number)


@router.get(
    "/Fleet/Equipment/{oemISOidentifier}/elements",
    responses={
        200: {"model": ElementShortList, "description": "Successful operation"},
        400: {"description": "Invalid parameter supplied"},
        404: {"description": "No element(s) found"},
    },
    tags=["Elements"],
    summary="Get all element_uid&#39;s between start and end date",
    response_model_by_alias=True,
)
async def get_elements_by_startdate_and_enddate(
    oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
    start_date: str = Query(None, description="Start time/date in UTC format", alias="start-date"),
    end_date: str = Query(None, description="End time/date in UTC format", alias="end-date"),
    page_number: int = Query(None, description="Page number, starting from 1", alias="page-number"),
    token_bearer: TokenModel = Security(
        get_token_bearer
    ),
) -> ElementShortList:
    """Returns all available elementids with names between start and endDate"""
    if not BaseElementsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseElementsApi.subclasses[0]().get_elements_by_startdate_and_enddate(oemISOidentifier, start_date, end_date, page_number)


@router.get(
    "/Fleet/Equipment/{oemISOidentifier}/elements/{element_uid}/header",
    responses={
        200: {"model": GetElementHeader, "description": "Successful operation"},
        400: {"description": "Invalid parameter supplied"},
        404: {"description": "No element(s) found"},
    },
    tags=["Elements"],
    summary="Get all header information / header parameter of element with uid",
    response_model_by_alias=True,
)
async def get_header(
    oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
    element_uid: str = Path(..., description="Unique Id of the element"),
    token_bearer: TokenModel = Security(
        get_token_bearer
    ),
) -> GetElementHeader:
    """Returns all header information about one element"""
    if not BaseElementsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseElementsApi.subclasses[0]().get_header(oemISOidentifier, element_uid)
