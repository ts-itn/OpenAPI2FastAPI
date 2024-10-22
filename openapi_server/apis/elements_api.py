# coding: utf-8
import logging
from typing import Dict, List  # noqa: F401
import importlib
import pkgutil
import httpx
from openapi_server.apis.elements_api_base import BaseElementsApi
import openapi_server.impl
import requests
from fastapi import Depends, HTTPException, Path, Query, Security
import requests
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
from collections import OrderedDict
from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.element import Element
from openapi_server.models.element_short_list import ElementShortList
from openapi_server.models.get_element_header import GetElementHeader
from openapi_server.models.get_event_data import GetEventData
from openapi_server.models.get_measurement_pass_series import GetMeasurementPassSeries
from openapi_server.models.getdata_series import GetdataSeries
from openapi_server.security_api import get_token_bearer
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from fastapi.security import HTTPBearer


load_dotenv()
router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)

class CustomLoginForm(BaseModel):
    username: str
    password: str

login_url = os.getenv('login_url', 'https://dacs.site/api/auth/login')

@router.post("/login")
async def login(form_data: CustomLoginForm = Depends()):
    global toker_global  # Declaring global to modify the global variable
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(login_url, json={
                "username": form_data.username,
                "password": form_data.password
            })
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=exc.response.status_code if exc.response else 500,
                                detail=str(exc)) from exc

        data = response.json()
        token = data.get("token")
        if not token:
            raise HTTPException(status_code=500, detail="Token not found in response")

        toker_global = token  # Save token in global variable (consider better alternatives for production)
        return {"token": toker_global}
    


asset_ids = []
to_assets = []
asset_ids_list=list(OrderedDict.fromkeys(asset_ids))
to_assets_list =list(OrderedDict.fromkeys(to_assets))

customerId = None
device_name = None
entityProfile = None
deviceId = None

@router.get("/get_token_info")
async def get_info(token_info: dict= Depends(get_token_bearer)):
    return token_info
    
customer_base_url = "https://dacs.site/api/customer/{customerId}/devices"
tenant_base_url = "https://dacs.site/api/tenant/devices" 
relationsDevice2Asset = "https://dacs.site/api/relations?fromId={YOUR_DEVICE_ID}&fromType=DEVICE"

def get_info_token(token_info: dict= Depends(get_token_bearer)):
    return token_info
@router.get(
    "/Fleet/Equipment/{oemISOidentifier}/elements",
    # responses={
    #     200: {"model": ElementShortList, "description": "Successful operation"},
    #     400: {"description": "Invalid parameter supplied"},
    #     404: {"description": "No element(s) found"},
    # },
    tags=["Elements"],
    summary="Get all element_uid's between start and end date",
    # response_model_by_alias=True,
)
async def get_elements_by_startdate_and_enddate(
    oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
    start_date: str = Query(None, description="Start time/date in UTC format", alias="start-date"),
    end_date: str = Query(None, description="End time/date in UTC format", alias="end-date"),
    page_number: int = Query(None, description="Page number, starting from 1", alias="page-number"),
    token_bearer: TokenModel = Security(get_token_bearer)):
    # ,
# ) -> ElementShortList:
    
   
    """Returns all available element IDs with names between start and endDate"""



    token_info = token_bearer
    tenant_admin = token_info.get("tenant_admin")
    customer_id = token_info.get("customer_id")

    headers = {"Authorization": f"Bearer {token_info['token']}"}
    

    if tenant_admin:
        device_name = oemISOidentifier
        tenant_url = tenant_base_url + f"?deviceName={device_name}"
        response = requests.get(tenant_url, headers=headers)
        deviceId = None 
        if response.status_code == 200:
            data = response.json()
            print("Received data:", data)
            logging.debug("Received data: %s", data)
            if data.get("customerId") is not None:
                 customerId = data.get("customerId").get("id")
            device_name = data.get("name") 
            if data.get("deviceProfileId") is not None:
                entityProfile = data.get("deviceProfileId").get("id")  
            if data.get("id")is not None:
                deviceId=data.get("id").get("id")
            
            relationsDevice_url = f"https://dacs.site/api/relations/info?fromId={deviceId}&fromType=DEVICE"


            payload = {
                "parameters": {
                    "fromId": deviceId,           # Ensure deviceId is correctly assigned
                    "fromType": "DEVICE",
                    "toType": "ASSET",
                    "direction": "FROM"           # Use "FROM" as per API requirements
                }
            }

            responseFromDevice = requests.get(relationsDevice_url, headers=headers)
            if responseFromDevice.status_code == 200:
                relations = responseFromDevice.json()
                for rel in relations:
                    if rel['to']['entityType'] == 'ASSET':
                        asset_id = rel['to']['id']
                        to_assest=rel['to']
                        if asset_id not in asset_ids:
                     
                            asset_ids.append(asset_id)
                        if to_assest not in to_assets:

                            to_assets.append(to_assest)
                return asset_ids
            else:
                print("Error:", responseFromDevice.status_code, responseFromDevice.text)
                raise HTTPException(status_code=responseFromDevice.status_code, detail=responseFromDevice.text)
        else:
            print("Error:", response.status_code, response.text)
            raise HTTPException(status_code=response.status_code, detail=response.text)

   
    else:
        page_size = 1
        page = page_number
        text_search = oemISOidentifier
        customer_url = customer_base_url.format(customerId=customer_id)
        params = {
            "pageSize": page_size,
            "page": page,
            "textSearch": text_search
        }

        response = requests.get(url=customer_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            print("Received data:", data)
            logging.debug("Received data: %s", data)
            if data.get("customerId") is not None:
               customerId = data.get("customerId").get("id")
            device_name = data.get("name") 
            if data.get("deviceProfileId") is not None:
                entityProfile = data.get("deviceProfileId").get("id")  
            if data.get("deviceId")is not None:
                deviceId=data.get("deviceId").get("id")
    
            return deviceId
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="No element(s) found")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)




# ###-------------------------------------------------------------------------------
# @router.get(
#     "/Fleet/Equipment/{oemISOidentifier}/elements/{element_uid}/data_series/",
#     responses={
#         200: {"model": GetdataSeries, "description": "Successful operation"},
#         400: {"description": "Invalid parameter supplied"},
#         404: {"description": "No element(s) found"},
#     },
#     tags=["Elements"],
#     summary="Get selected data_series of element with uid",
#     response_model_by_alias=True,
# )
# async def get_element_data_series(
#     oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
#     element_uid: str = Path(..., description="Unique Id of the element"),
#     page_number: int = Query(None, description="Page number, starting from 1", alias="page-number"),
#     token_bearer: TokenModel = Security(
#         get_token_bearer
#     ),
# ) -> GetdataSeries:
#     """Returns requested dataseries from the list about one element"""
#     if not BaseElementsApi.subclasses:
#         raise HTTPException(status_code=500, detail="Not implemented")
#     return await BaseElementsApi.subclasses[0]().get_element_data_series(oemISOidentifier, element_uid, page_number)


# @router.get(
#     "/Fleet/Equipment/{oemISOidentifier}/elements/{element_uid}",
#     responses={
#         200: {"model": Element, "description": "Successful operation"},
#         400: {"description": "Invalid parameter supplied"},
#         404: {"description": "No element(s) found"},
#     },
#     tags=["Elements"],
#     summary="Get all values of element with uid",
#     response_model_by_alias=True,
# )
# async def get_element_details(
#     oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
#     element_uid: str = Path(..., description="unique Id of the element"),
#     page_number: int = Query(None, description="Page number, starting from 1", alias="page-number"),
#     token_bearer: TokenModel = Security(
#         get_token_bearer
#     ),
# ) -> Element:
#     """Returns all information about one element"""
#     if not BaseElementsApi.subclasses:
#         raise HTTPException(status_code=500, detail="Not implemented")
#     return await BaseElementsApi.subclasses[0]().get_element_details(oemISOidentifier, element_uid, page_number)


# @router.get(
#     "/Fleet/Equipment/{oemISOidentifier}/elements/{element_uid}/event_data/",
#     responses={
#         200: {"model": GetEventData, "description": "Successful operation"},
#         400: {"description": "Invalid parameter supplied"},
#         404: {"description": "No element(s) found"},
#     },
#     tags=["Elements"],
#     summary="Get all event data of element with uid",
#     response_model_by_alias=True,
# )
# async def get_element_event_data(
#     oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
#     element_uid: str = Path(..., description="unique Id of the element"),
#     page_number: int = Query(None, description="Page number, starting from 1", alias="page-number"),
#     token_bearer: TokenModel = Security(
#         get_token_bearer
#     ),
# ) -> GetEventData:
#     """Returns requested event data about one element"""
#     if not BaseElementsApi.subclasses:
#         raise HTTPException(status_code=500, detail="Not implemented")
#     return await BaseElementsApi.subclasses[0]().get_element_event_data(oemISOidentifier, element_uid, page_number)


# @router.get(
#     "/Fleet/Equipment/{oemISOidentifier}/elements/{element_uid}/measurement_pass/",
#     responses={
#         200: {"model": GetMeasurementPassSeries, "description": "Successful operation"},
#         400: {"description": "Invalid parameter supplied"},
#         404: {"description": "No element(s) found"},
#     },
#     tags=["Elements"],
#     summary="Get all data_series of a measurement pass of element with uid",
#     response_model_by_alias=True,
# )
# async def get_element_meassurement_data_series(
#     oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
#     element_uid: str = Path(..., description="unique Id of the element"),
#     page_number: int = Query(None, description="Page number, starting from 1", alias="page-number"),
#     token_bearer: TokenModel = Security(
#         get_token_bearer
#     ),
# ) -> GetMeasurementPassSeries:
#     """Returns requested measurement pass dataseries about one element"""
#     if not BaseElementsApi.subclasses:
#         raise HTTPException(status_code=500, detail="Not implemented")
#     return await BaseElementsApi.subclasses[0]().get_element_meassurement_data_series(oemISOidentifier, element_uid, page_number)





# @router.get(
#     "/Fleet/Equipment/{oemISOidentifier}/elements/{element_uid}/header",
#     responses={
#         200: {"model": GetElementHeader, "description": "Successful operation"},
#         400: {"description": "Invalid parameter supplied"},
#         404: {"description": "No element(s) found"},
#     },
#     tags=["Elements"],
#     summary="Get all header information / header parameter of element with uid",
#     response_model_by_alias=True,
# )
# async def get_header(
#     oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
#     element_uid: str = Path(..., description="Unique Id of the element"),
#     token_bearer: TokenModel = Security(
#         get_token_bearer
#     ),
# ) -> GetElementHeader:
#     """Returns all header information about one element"""
#     if not BaseElementsApi.subclasses:
#         raise HTTPException(status_code=500, detail="Not implemented")
#     return await BaseElementsApi.subclasses[0]().get_header(oemISOidentifier, element_uid)
