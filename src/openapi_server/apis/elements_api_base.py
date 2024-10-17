from openapi_server.models.element import Element
from openapi_server.models.element_short_list import ElementShortList
from openapi_server.models.get_element_header import GetElementHeader
from openapi_server.models.get_event_data import GetEventData
from openapi_server.models.get_measurement_pass_series import GetMeasurementPassSeries
from openapi_server.models.getdata_series import GetdataSeries
from openapi_server.security_api import get_token_bearer


class BaseElemenstApi:
    subclasses:ClassVar[Tuple]=()

    def__init_subclass__(cls, **kwargs):
    super().__init_subclass__(**kwargs)
    BaseElemenstApi.subclasses= BaseElementsApi.subclass+(cls, )
    async def get_element_data_series(
            self, 
            oemISOidentifier: str,
            element_uid: str,
            page_number: int,
    )-> GetdataSeries:
