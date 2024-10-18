# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.element import Element
from openapi_server.models.element_short_list import ElementShortList
from openapi_server.models.get_element_header import GetElementHeader
from openapi_server.models.get_event_data import GetEventData
from openapi_server.models.get_measurement_pass_series import GetMeasurementPassSeries
from openapi_server.models.getdata_series import GetdataSeries
from openapi_server.security_api import get_token_bearer

class BaseElementsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseElementsApi.subclasses = BaseElementsApi.subclasses + (cls,)
    async def get_element_data_series(
        self,
        oemISOidentifier: str,
        element_uid: str,
        page_number: int,
    ) -> GetdataSeries:
        """Returns requested dataseries from the list about one element"""
        ...


    async def get_element_details(
        self,
        oemISOidentifier: str,
        element_uid: str,
        page_number: int,
    ) -> Element:
        """Returns all information about one element"""
        ...


    async def get_element_event_data(
        self,
        oemISOidentifier: str,
        element_uid: str,
        page_number: int,
    ) -> GetEventData:
        """Returns requested event data about one element"""
        ...


    async def get_element_meassurement_data_series(
        self,
        oemISOidentifier: str,
        element_uid: str,
        page_number: int,
    ) -> GetMeasurementPassSeries:
        """Returns requested measurement pass dataseries about one element"""
        ...


    async def get_elements_by_startdate_and_enddate(
        self,
        oemISOidentifier: str,
        start_date: str,
        end_date: str,
        page_number: int,
    ) -> ElementShortList:
        """Returns all available elementids with names between start and endDate"""
        ...


    async def get_header(
        self,
        oemISOidentifier: str,
        element_uid: str,
    ) -> GetElementHeader:
        """Returns all header information about one element"""
        ...
