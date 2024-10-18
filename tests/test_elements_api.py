# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.element import Element  # noqa: F401
from openapi_server.models.element_short_list import ElementShortList  # noqa: F401
from openapi_server.models.get_element_header import GetElementHeader  # noqa: F401
from openapi_server.models.get_event_data import GetEventData  # noqa: F401
from openapi_server.models.get_measurement_pass_series import GetMeasurementPassSeries  # noqa: F401
from openapi_server.models.getdata_series import GetdataSeries  # noqa: F401


def test_get_element_data_series(client: TestClient):
    """Test case for get_element_data_series

    Get selected data-series of element with uid
    """
    params = [("page_number", 1)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/Fleet/Equipment/{oemISOidentifier}/elements/{elementuid}/data-series/".format(oemISOidentifier='7RM32YG4M00007328', element_uid='element_uid_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_element_details(client: TestClient):
    """Test case for get_element_details

    Get all values of element with uid
    """
    params = [("page_number", 56)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/Fleet/Equipment/{oemISOidentifier}/elements/{element-uid}".format(oemISOidentifier='7RM32YG4M00007328', element-uid='element_uid_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_element_event_data(client: TestClient):
    """Test case for get_element_event_data

    Get all event data of element with uid
    """
    params = [("page_number", 1)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/Fleet/Equipment/{oemISOidentifier}/elements/{element-uid}/event-data/".format(oemISOidentifier='7RM32YG4M00007328', element-uid='element_uid_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_element_meassurement_data_series(client: TestClient):
    """Test case for get_element_meassurement_data_series

    Get all data-series of a measurement pass of element with uid
    """
    params = [("page_number", 1)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/Fleet/Equipment/{oemISOidentifier}/elements/{element-uid}/measurement-pass/".format(oemISOidentifier='7RM32YG4M00007328', element-uid='element_uid_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_elements_by_startdate_and_enddate(client: TestClient):
    """Test case for get_elements_by_startdate_and_enddate

    Get all element-uid's between start and end date
    """
    params = [("start_date", ' 2023-04-23T17:25:43.511Z'),     ("end_date", ' 2023-04-23T18:25:43.511Z'),     ("page_number", 1)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/Fleet/Equipment/{oemISOidentifier}/elements".format(oemISOidentifier='7RM32YG4M00007328'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_header(client: TestClient):
    """Test case for get_header

    Get all header information / header parameter of element with uid
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/Fleet/Equipment/{oemISOidentifier}/elements/{element-uid}/header".format(oemISOidentifier='7RM32YG4M00007328', element-uid='element_uid_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

