# coding: utf-8
import logging
import asyncio
import math
import os
from datetime import datetime
from typing import List, Dict, Any, Set

import httpx
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Security
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from dotenv import load_dotenv

from openapi_server.models.element_short_list import ElementShortList
from openapi_server.models.element import Element
from openapi_server.security_api import get_token_bearer

load_dotenv()
router = APIRouter()
login_url = os.getenv('login_url', 'https://dacs.site/api/auth/login')

class CustomLoginForm(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(form_data: CustomLoginForm = Depends()):
    global token_global
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
        token_global = token
        return {"token": token_global}

async def fetch_device_id(client: httpx.AsyncClient, headers: Dict[str, str], oemISOidentifier: str, tenant_admin: bool, customer_id: str) -> str:
    if tenant_admin:
        # Logic for tenant admin
        tenant_url = f"https://dacs.site/api/tenant/devices?deviceName={oemISOidentifier}"
        response = await client.get(tenant_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise HTTPException(status_code=404, detail="Device not found")
        device_id = data.get("id", {}).get("id")
        if not device_id:
            raise HTTPException(status_code=404, detail="Device ID not found")
        return device_id
    else:
        # Logic for customer
        page_size = 100
        page = 0
        customer_url = f"https://dacs.site/api/customer/{customer_id}/devices"
        params = {
            "pageSize": page_size,
            "page": page,
            "textSearch": oemISOidentifier,
        }
        response = await client.get(customer_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if not data or "data" not in data:
            raise HTTPException(status_code=404, detail="Device not found")
        devices = data["data"]
        for device in devices:
            if device.get("name") == oemISOidentifier:
                device_id = device.get("id", {}).get("id")
                if device_id:
                    return device_id
        raise HTTPException(status_code=404, detail="Device not found")

async def fetch_asset_ids(client: httpx.AsyncClient, headers: Dict[str, str], device_id: str) -> Set[str]:
    relations_url = f"https://dacs.site/api/relations/info?fromId={device_id}&fromType=DEVICE"
    response = await client.get(relations_url, headers=headers)
    response.raise_for_status()
    relations = response.json()
    if not relations:
        raise HTTPException(status_code=404, detail="No asset relations found for device")
    asset_ids = set()
    for rel in relations:
        if rel.get('to', {}).get('entityType') == 'ASSET':
            asset_id = rel.get('to', {}).get('id')
            if asset_id:
                asset_ids.add(asset_id)
    if not asset_ids:
        raise HTTPException(status_code=404, detail="No assets found")
    return asset_ids

async def fetch_telemetry(client: httpx.AsyncClient, headers: Dict[str, str], asset_id: str, start_time_millis: int, end_time_millis: int, telemetry_keys: List[str]) -> Dict[str, Any]:
    keys_str = ",".join(telemetry_keys)
    url = (
        f"https://dacs.site/api/plugins/telemetry/ASSET/{asset_id}/values/timeseries"
        f"?keys={keys_str}&startTs={start_time_millis}&endTs={end_time_millis}"
    )
    response = await client.get(url, headers=headers)
    response.raise_for_status()
    telemetry = response.json()
    return telemetry

async def fetch_telemetries(client: httpx.AsyncClient, headers: Dict[str, str], asset_ids: Set[str], start_time_millis: int, end_time_millis: int, telemetry_keys: List[str]) -> List[Dict[str, Any]]:
    tasks = [
        fetch_telemetry(client, headers, asset_id, start_time_millis, end_time_millis, telemetry_keys)
        for asset_id in asset_ids
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    telemetries = []
    for result in results:
        if isinstance(result, Exception):
            # Log the exception and continue
            logging.error("Error fetching telemetry: %s", result)
        else:
            telemetries.append(result)
    return telemetries

def process_telemetries(telemetries: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    short_list = []
    seen_identifiers = set()
    for telemetry in telemetries:
        if not telemetry:
            continue
        try:
            dw_counter = telemetry['dw_counter'][0]['value']
            s_index = telemetry['s_index'][0]['value']
            pfahl = telemetry['pfahl'][0]['value']
            element_name = f"{dw_counter}{s_index}"
            element_uid = pfahl
            identifier = (element_name, element_uid)
            if identifier not in seen_identifiers:
                seen_identifiers.add(identifier)
                short_list.append({
                    "elementName": element_name,
                    "elementUid": element_uid
                })
        except (KeyError, IndexError) as e:
            logging.error("Error processing telemetry data: %s", e)
            continue
    return short_list

def paginate_list(data_list: List[Any], page_number: int, page_size: int = 100) -> (List[Any], int):
    total_items = len(data_list)
    total_pages = max(1, math.ceil(total_items / page_size))
    if page_number < 1 or page_number > total_pages:
        return [], total_items
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    paginated_list = data_list[start_index:end_index]
    return paginated_list, total_items

@router.get(
    "/Fleet/Equipment/{oemISOidentifier}/elements",
    responses={
        200: {"model": ElementShortList, "description": "Successful operation"},
        400: {"description": "Invalid parameter supplied"},
        404: {"description": "No element(s) found"},
    },
    tags=["Elements"],
    summary="Get all element_uid's between start and end date",
    response_model_by_alias=True,
)
async def get_elements_by_startdate_and_enddate(
    oemISOidentifier: str = Path(..., description="OEM ISO identifier, as defined in ISO 15143-3"),
    start_date: str = Query(None, description="Start time/date in UTC format", alias="start-date"),
    end_date: str = Query(None, description="End time/date in UTC format", alias="end-date"),
    page_number: int = Query(1, description="Page number, starting from 1", alias="page-number"),
    token_bearer: dict = Security(get_token_bearer)
) -> ElementShortList:
    telemetry_keys = ["pfahl", "s_index", "dw_counter"]
    try:
        utc_time_start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        start_time_millis = int(utc_time_start.timestamp() * 1000)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Start time is not in the correct format. It should be '%Y-%m-%dT%H:%M:%S.%fZ'"
        )
    try:
        utc_time_stop = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        end_time_millis = int(utc_time_stop.timestamp() * 1000)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="End time is not in the correct format. It should be '%Y-%m-%dT%H:%M:%S.%fZ'"
        )
    token_info = token_bearer
    tenant_admin = token_info.get("tenant_admin", False)
    customer_id = token_info.get("customer_id")
    headers = {"Authorization": f"Bearer {token_info['token']}"}
    async with httpx.AsyncClient() as client:
        try:
            device_id = await fetch_device_id(client, headers, oemISOidentifier, tenant_admin, customer_id)
            asset_ids = await fetch_asset_ids(client, headers, device_id)
            telemetries = await fetch_telemetries(client, headers, asset_ids, start_time_millis, end_time_millis, telemetry_keys)
            short_list = process_telemetries(telemetries)
            paginated_list, total_items = paginate_list(short_list, page_number, page_size=100)
            total_pages = max(1, math.ceil(total_items / 100))
            if not paginated_list:
                raise HTTPException(status_code=404, detail="No element(s) found on this page")
            statistics = {
                "totalPages": total_pages,
                "pageSize": len(paginated_list),
                "currentPage": page_number
            }
            prev_link = None
            if page_number > 1:
                prev_link = {"href": f"/Fleet/Equipment/{oemISOidentifier}/elements?start-date={start_date}&end-date={end_date}&page-number={page_number - 1}"}
            next_link = None
            if page_number < total_pages:
                next_link = {"href": f"/Fleet/Equipment/{oemISOidentifier}/elements?start-date={start_date}&end-date={end_date}&page-number={page_number + 1}"}
            combined_data = {
                "ShortList": paginated_list,
                "statistics": statistics,
                "prevLink": prev_link,
                "nextLink": next_link
            }
            return combined_data
        except HTTPException as he:
            raise he
        except Exception as e:
            logging.exception("An unexpected error occurred")
            raise HTTPException(status_code=500, detail="Internal server error")
