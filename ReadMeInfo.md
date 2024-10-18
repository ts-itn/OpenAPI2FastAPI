# Introduction

# Project Structure

# Detailed File Descriptions

### `.openapi-generator`

### `main.py`

### `src/openapi_server/`

#### apis/
- **`__init__.py` in apis/**: Initializes the API package.
- **`elements_api_base.py`**: Base class for the elements API with core methods for elements functionality.
- **`elements_api.py`**: Implements routes and links them to the base class methods.

#### impl/
- **`__init__.py` in impl/**: Initializes the `impl` package where the core logic is implemented.

#### models/
- **`__init__.py` in models/**: Initializes the models package that contains all the data models used across the API.

### Model Files
- **`data_unit.py`**: Defines the structure of individual units of data (e.g., timestamp, depth).
- **`element.py`**: Defines the full element, including its data series, header, event data, etc.
- **`element_header.py`**: Metadata about the element (e.g., ID, working method, machine type).
- **`element_short.py`**: A shorter version of the element, used in lists.
- **`element_short_list.py`**: A list of short element models, with pagination links and statistics.
- **`event_data_unit.py`**: Defines event data associated with an element, such as start/end times.
- **`extra_models.py`**: Contains additional models, such as token models for security.
- **`get_element_header.py`**: Defines the structure for retrieving the header of an element.
- **`get_event_data.py`**: Defines the structure for retrieving event data about an element.
- **`get_measurement_pass_series.py`**: Structure for retrieving a measurement pass data series.
- **`getdata_series.py`**: Structure for retrieving a series of data for a specific element.
- **`link.py`**: Defines links used for pagination or navigation between API responses.
- **`measurement_pass_unit.py`**: Defines individual measurement pass data units, such as depth and deviation.
- **`statistics.py`**: Defines pagination statistics, such as total pages, current page, and page size.

# How the Files Interact

# Additional Notes

# Conclusion



#### Introduction
This project is an API server generated from an OpenAPI specification for the MiC4.0 Element API Cluster special foundation. It is designed to facilitate machine data exchange in the construction sector, specifically for special foundation engineering.

The API allows clients to retrieve data about construction elements, including their details, data series, event data, and measurement pass data. The server is built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.7+.


## Project Structure
```
.openapi-generator
main.py
src/
└── openapi_server/
    ├── apis/
    │   ├── __init__.py
    │   ├── elements_api_base.py
    │   ├── elements_api.py
    │   └── impl/
    │       └── __init__.py
    └── models/
        ├── __init__.py
        ├── data_unit.py
        ├── element.py
        ├── element_header.py
        ├── element_short.py
        ├── element_short_list.py
        ├── event_data_unit.py
        ├── extra_models.py
        ├── get_element_header.py
        ├── get_event_data.py
        ├── get_measurement_pass_series.py
        ├── getdata_series.py
        ├── link.py
        ├── measurement_pass_unit.py
        └── statistics.py

```

### Detailed File Descriptions

### **.openapi-generator**
- **Purpose**: This is a configuration file used by the OpenAPI Generator tool.
- **Functionality**:
  - Specifies settings for code generation, such as package names, generator types, and other options.
  - Ensures that the generated code adheres to specific project requirements.
- **Importance**:
  - Essential for regenerating code if the OpenAPI specification changes.
  - Helps maintain consistency across generated code.

### **main.py**
- **Purpose**: Acts as the entry point of the application.
- **Functionality**:
  - Initializes the FastAPI application.
  - Includes API routers from the `apis/` directory.
  - Configures middleware, exception handlers, and startup events if necessary.
  - Runs the server when executed.
- **Key Components**:
  - `app`: An instance of FastAPI.
  - Inclusion of routers, e.g., `app.include_router(elements_api.router)`.
  - Conditional `if __name__ == "__main__":` block to run the server using `uvicorn`.

```
from fastapi import FastAPI
from openapi_server.apis import elements_api

app = FastAPI()

app.include_router(elements_api.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
```
### **src/openapi_server/**
- **Purpose**: This is the main package containing the server implementation, including API endpoint definitions and data models.

### **elements_api_base.py**
- **Purpose**: Defines the abstract base class `BaseElementsApi` for the Elements API.
- **Functionality**:
  - Declares abstract methods corresponding to each API endpoint related to elements.
  - Serves as a contract for implementing classes to ensure all endpoints are implemented.
- **Key Components**:
  - **Class**: `BaseElementsApi`
  - Uses `ClassVar` to keep track of subclasses.
  - Abstract methods for each endpoint:
    - `get_element_data_series`
    - `get_element_details`
    - `get_element_event_data`
    - `get_element_meassurement_data_series`
    - `get_elements_by_startdate_and_enddate`
    - `get_header`
- **Security**:
  - Uses `get_token_bearer` from `openapi_server.security_api` to handle authentication.
- **Type Annotations**:
  - Uses models from `openapi_server.models` for request and response types.

#### Example of an Abstract Method:

```python
async def get_element_details(
    self,
    oemISOidentifier: str,
    element_uid: str,
    page_number: int,
) -> Element:
    """Returns all information about one element"""
    ...
```
#### Usage:
Implement this base class in a subclass to provide concrete implementations for the abstract methods. 

## **elements_api.py**
- **Purpose**: Contains the FastAPI router with the actual API endpoint definitions.
- **Functionality**:
  - Defines the HTTP routes and links them to the methods defined in `BaseElementsApi`.
  - Handles request parameter extraction, response formatting, and exception handling.
- **Key Components**:
  - **Router**: An instance of `APIRouter`.
  - **Endpoint Definitions**:
    - Decorated with HTTP method decorators (e.g., `@router.get`).
    - Include path parameters and query parameters.
  - **Security**:
    - Uses `Security` dependencies and `get_token_bearer` to handle authentication.
- **Dynamic Import**:
  - Imports implementation modules from `openapi_server.impl` to find subclasses of `BaseElementsApi`.
- **Error Handling**:
  - Raises `HTTPException` with status code 500 if no implementation is found.

#### Example of an Abstract Method:
```python
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
```

#### Explanation:

- **Path Parameters**:
  - `oemISOidentifier`: Identifier of the equipment manufacturer.
  - `element_uid`: Unique identifier of the element.
  
- **Query Parameters**:
  - `page_number`: For pagination, defaults to `None`.

- **Security**:
  - Requires a token provided by `token_bearer`.

- **Response**:
  - Returns an instance of the `Element` model.

- **Implementation**:
  - Calls the corresponding method in the first subclass of `BaseElementsApi`.

## **impl/**
- **Purpose**: Contains implementation classes that provide concrete implementations of the abstract methods in `BaseElementsApi`.

#### **__init__.py in impl/**
- **Purpose**: Marks the `impl/` directory as a Python package.
- **Functionality**:
  - May include code to dynamically import all implementation modules.
  - Ensures that all subclasses of `BaseElementsApi` are registered.
- **Importance**:
  - Allows the API router to find and use the concrete implementations.

### **models/**
- **Purpose**: Contains data model classes that represent the structures of the data being sent and received by the API. The models are defined using Pydantic, which provides data validation and settings management.

#### **__init__.py in models/**
- **Purpose**: Marks the `models/` directory as a Python package.
- **Functionality**:
  - May import models to make them accessible when importing the package.
  - Facilitates easier imports in other parts of the application.

- **Example**:

```python
from .data_unit import DataUnit
from .element import Element
# and so on for each model
```

# Model Files
Below are descriptions of each model file in the `models/` directory:

### **data_unit.py**
- **Purpose**: Defines the `DataUnit` class, which represents a single unit of time-series data related to an element.
- **Functionality**:
  - Contains fields representing various measurements collected at a specific timestamp.
  - Provides data validation and serialization/deserialization methods.
- **Key Fields**:
  - `timestamp`: The timestamp with timezone of this data unit.
  - `depth`: Depth measurement in meters with sign.
- **Other Measurements**:
  - `leader_inclination_x` and `leader_inclination_y`: Inclination angles.
  - `drilling_torque`: Torque during drilling.
  - `crowd_force`: Force applied during drilling.
  - `rotation_speed_rotary_drive`: Speed of the rotary drive.
  - Additional fields for specific drilling methods.

```python
class DataUnit(BaseModel):
    timestamp: datetime = Field(description="The timestamp with timezone of this dataUnit")
    depth: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Depth measurement in meters with sign")
    # ... other fields ...
```
#### **Methods**:

- **`to_str()`**: Returns the string representation of the `DataUnit` instance.
- **`to_json()`**: Returns the JSON representation of the `DataUnit` instance.
- **`from_json()`**: Creates an instance of `DataUnit` from a JSON string.
- **`to_dict()`**: Returns a dictionary representation of the `DataUnit` instance.
- **`from_dict()`**: Creates an instance of `DataUnit` from a dictionary.

### **element.py**
- **Purpose**: Defines the `Element` class, representing detailed information about an element, including headers and associated data series.
- **Functionality**:
  - Aggregates data from various related models into a comprehensive representation of an element.
- **Key Fields**:
  - `element_header`: An instance of `ElementHeader`.
  - `data_series`: A list of `DataUnit` instances.
  - `event_data`: Optional list of `EventDataUnit`.
  - `measurement_pass_series`: Optional list of `MeasurementPassUnit`.
  - `statistics`: Pagination and statistical information.
  - `prev_link`, `next_link`: Hyperlinks for pagination.
```python
class Element(BaseModel):
    element_header: ElementHeader = Field(alias="elementHeader")
    data_series: List[DataUnit] = Field(alias="dataSeries")
    event_data: Optional[List[EventDataUnit]] = Field(default=None, alias="eventData")
    # ... other fields ...
```
### Usage:

Used as a response model when returning detailed element information via the API.

## **element.py**
- **Purpose**: Defines the `Element` class, representing detailed information about an element, including headers and associated data series.
- **Functionality**:
  - Aggregates data from various related models into a comprehensive representation of an element.
- **Key Fields**:
  - `element_header`: An instance of `ElementHeader`.
  - `data_series`: A list of `DataUnit` instances.
  - `event_data`: Optional list of `EventDataUnit`.
  - `measurement_pass_series`: Optional list of `MeasurementPassUnit`.
  - `statistics`: Pagination and statistical information.
  - `prev_link`, `next_link`: Hyperlinks for pagination.

- **Usage**:
  - Used as a response model when returning detailed element information via the API.

## **element_header.py**
- **Purpose**: Defines the `ElementHeader` class, containing metadata and descriptive information about an element.
- **Functionality**:
  - Holds general information that applies to the entire element, such as identifiers and timestamps.
- **Key Fields**:
  - `element_unique_id`: Unique identifier for the element.
  - `working_method`: The method or procedure used (e.g., Kelly drilling, Impact pile driving).
  - `machine_type`: Machine make and model information.
  - `element_number`: The name or number of the element (e.g., pile number).
  - `record_start_date_time` and `record_stop_date_time`: Timestamps for the start and end of data recording.
  - `operator_id`: Name of the operator.
  - `jobsite`: Name of the job site.

```python
class ElementHeader(BaseModel):
    element_unique_id: Optional[StrictStr] = Field(default=None, description="Unique ID", alias="elementUniqueID")
    working_method: Optional[StrictStr] = Field(default=None, description="Working method used", alias="workingMethod")
    # ... other fields ...
```
## **element_short.py**
- **Purpose**: Defines the `ElementShort` class, a simplified representation of an element containing minimal information.
- **Functionality**:
  - Used to list elements without loading all detailed data.
- **Key Fields**:
  - `element_name`: Name of the element.
  - `element_uid`: Unique identifier for the element.

```python
class ElementShort(BaseModel):
    element_name: StrictStr = Field(alias="elementName")
    element_uid: StrictStr = Field(description="Unique ID", alias="elementUid")
```

### **element_short_list.py**
- **Purpose**: Defines the `ElementShortList` class, which encapsulates a list of `ElementShort` instances.
- **Functionality**:
  - Used to return paginated lists of elements.
- **Key Fields**:
  - `short_list`: A list of `ElementShort` instances.
  - `statistics`: Pagination and statistical information.
  - `prev_link`, `next_link`: Hyperlinks for pagination.
```python
class ElementShortList(BaseModel):
    short_list: List[ElementShort] = Field(alias="ShortList")
    statistics: Optional[Statistics] = None
    prev_link: Optional[Link] = Field(default=None, alias="prevLink")
    next_link: Optional[Link] = Field(default=None, alias="nextLink")
```

## **event_data_unit.py**
- **Purpose**: Defines the `EventDataUnit` class, representing an event associated with an element.
- **Functionality**:
  - Captures events that occur during the element's lifecycle, such as status changes or comments.
- **Key Fields**:
  - `status_start`: Start timestamp of the event.
  - `status_end`: End timestamp of the event.
  - `comment`: Optional comment describing the event.
```python
class EventDataUnit(BaseModel):
    status_start: Optional[datetime] = Field(default=None, alias="statusStart")
    status_end: Optional[datetime] = Field(default=None, alias="statusEnd")
    comment: Optional[StrictStr] = Field(default=None, description="General comment")
```
## **extra_models.py**
- **Purpose**: Contains additional models that may not be directly generated from the OpenAPI specification.
- **Functionality**:
  - Defines custom models used in the application.
- **Key Components**:
  - **`TokenModel`**: Defines a simple token model used for authentication purposes.
```python
class TokenModel(BaseModel):
    """Defines a token model."""
    sub: str
```
## **get_element_header.py**
- **Purpose**: Defines the `GetElementHeader` class, used as a response model when retrieving an element's header information.
- **Functionality**:
  - Wraps the `ElementHeader` model for API responses.
- **Key Fields**:
  - `element_header`: An instance of `ElementHeader`.
```python
class GetElementHeader(BaseModel):
    element_header: ElementHeader = Field(alias="elementHeader")
```
## **get_event_data.py**
- **Purpose**: Defines the `GetEventData` class, used as a response model for retrieving event data associated with an element.
- **Functionality**:
  - Encapsulates event data along with pagination information.
- **Key Fields**:
  - `event_data`: A list of `EventDataUnit` instances.
  - `statistics`: Pagination information.
  - `prev_link`, `next_link`: Hyperlinks for pagination.

```python
class GetEventData(BaseModel):
    event_data: List[EventDataUnit] = Field(alias="eventData")
    statistics: Optional[Statistics] = None
    prev_link: Optional[Link] = Field(default=None, alias="prevLink")
    next_link: Optional[Link] = Field(default=None, alias="nextLink")
```
## **get_measurement_pass_series.py**
- **Purpose**: Defines the `GetMeasurementPassSeries` class, representing a collection of measurement pass data for an element.
- **Functionality**:
  - Used to return measurement pass data with pagination.
- **Key Fields**:
  - `measurement_pass_series`: A list of `MeasurementPassUnit` instances.
  - `statistics`: Pagination information.
  - `prev_link`, `next_link`: Hyperlinks for pagination.
```python
class GetMeasurementPassSeries(BaseModel):
    measurement_pass_series: List[MeasurementPassUnit] = Field(alias="measurementPassSeries")
    statistics: Optional[Statistics] = None
    prev_link: Optional[Link] = Field(default=None, alias="prevLink")
    next_link: Optional[Link] = Field(default=None, alias="nextLink")
```
## **getdata_series.py**
- **Purpose**: Defines the `GetdataSeries` class, used as a response model when retrieving data series for an element.
- **Functionality**:
  - Wraps a list of `DataUnit` instances for API responses.
- **Key Fields**:
  - `data_series`: A list of `DataUnit` instances.
  - `statistics`: Pagination information.
  - `prev_link`, `next_link`: Hyperlinks for pagination
```python
class GetdataSeries(BaseModel):
    data_series: List[DataUnit] = Field(alias="dataSeries")
    statistics: Optional[Statistics] = None
    prev_link: Optional[Link] = Field(default=None, alias="prevLink")
    next_link: Optional[Link] = Field(default=None, alias="nextLink")
```
## **link.py**
- **Purpose**: Defines the `Link` class, representing a hyperlink for pagination or resource linking.
- **Functionality**:
  - Used in models to provide navigational links in API responses.
- **Key Fields**:
  - `href`: The URL of the linked resource.
```python
class Link(BaseModel):
    href: Optional[StrictStr] = Field(default=None, description="Hypermedia reference URL")
```
## **measurement_pass_unit.py**
- **Purpose**: Defines the `MeasurementPassUnit` class, representing a single measurement pass data point.
- **Functionality**:
  - Captures measurements collected during a specific pass in measurement-intensive processes.
- **Key Fields**:
  - `timestamp`: The timestamp of the measurement.
  - `depth`: Depth measurement with sign.
  - `lowering_speed`: Speed at which the equipment is lowered.
  - `deviation_x` and `deviation_y`: Deviations in X and Y axes.
  - `rotation_z`: Rotation around the Z-axis.
  - `inclination_x` and `inclination_y`: Inclination angles.
```python
class MeasurementPassUnit(BaseModel):
    timestamp: Optional[datetime] = None
    depth: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Depth measurement")
    # ... other fields ...
```
#### **statistics.py**
- **Purpose**: Defines the `Statistics` class, containing pagination and statistical information about a collection of data.
- **Functionality**:
  - Provides context about the dataset, useful for client-side pagination.
- **Key Fields**:
  - `total_pages`: Total number of pages available.
  - `page_size`: Number of items per page.
  - `current_page`: The current page number.
```python
class Statistics(BaseModel):
    total_pages: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, alias="totalPages")
    page_size: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, alias="pageSize")
    current_page: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, alias="currentPage")
```
# How the Files Interact

### API Layer:
- `elements_api.py` defines the API endpoints using FastAPI.
- It relies on abstract methods from `elements_api_base.py`.
- Concrete implementations are expected from classes in the `impl/` directory.

### Models:
- Data models in the `models/` directory are used for:
  - Type annotations in endpoint functions.
  - Parsing incoming request data.
  - Formatting outgoing response data.
- Models ensure data consistency and perform validation.

### Main Application:
- `main.py` initializes the FastAPI app and includes routers from the `apis/` directory.
- When the server runs, it listens for HTTP requests and routes them to the appropriate endpoint handlers.

### OpenAPI Generator Configuration:
- The `.openapi-generator` file configures code generation settings.
- Ensures that generated code matches the project's structure and standards.
- If the OpenAPI specification changes, code can be regenerated using this configuration.

### Security:
- Authentication is handled using security dependencies, such as `get_token_bearer`.
- The `TokenModel` in `extra_models.py` defines the expected structure of authentication tokens.

---

# Additional Notes

### Authentication:
- The API uses token-based authentication.
- Security dependencies are applied to endpoints to enforce authentication.
- Ensure that `get_token_bearer` is properly implemented to validate tokens.

### Pagination:
- Many response models include pagination fields (`statistics`, `prev_link`, `next_link`).
- The API supports paginated responses for collections.
- Clients can navigate through pages using the provided links.

### Data Validation:
- Models use Pydantic, which provides robust data validation.
- Incoming data is validated against the model schemas.
- Validation errors are automatically returned as HTTP 422 responses.

### Extensibility:
- The use of abstract base classes and an `impl/` directory allows for easy extensibility.
- Developers can provide custom implementations for the API endpoints by subclassing `BaseElementsApi`.

### Dynamic Implementation Loading:
- The API dynamically imports implementation modules from the `impl/` package.
- This allows for plug-and-play of different implementations without modifying the core API definitions.

---

# Conclusion

This project provides a structured API server with well-defined endpoints and data models, generated from an OpenAPI specification. Each file plays a specific role in handling API requests, data validation, and response formatting. By understanding the purpose and functionality of each file, developers can effectively maintain, extend, and utilize the application.

Whether you're adding new features, fixing bugs, or integrating this API into another system, this documentation should serve as a comprehensive guide to help you navigate the codebase with confidence.
