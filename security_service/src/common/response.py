import json
from datetime import datetime
from typing import TypeVar, Generic

from fastapi import status
from pydantic import BaseModel

T = TypeVar("T")


class Pagination(BaseModel):
    limit: int
    offset: int
    total: int


class MetaData(BaseModel):
    server_time: datetime | str = datetime.now()
    has_error: bool = False
    message: str
    pagination: Pagination | None = None

    class Config:
        from_attributes = True


# Define the main response model which accepts any data type in the `data` field
class ApiResponse(BaseModel, Generic[T]):
    meta: MetaData
    data: T


def get_standard_response(message, has_error=False, data=None):
    meta = MetaData(
        server_time=datetime.now().isoformat(),  # Convert datetime to ISO 8601 string
        has_error=has_error,
        message=message,
    )
    response = ApiResponse(meta=meta, data=data)
    return response.dict()  # Convert Pydantic model to dictionary


class ResponseMessages:
    def __init__(self, object_name: str):
        self.object_name = object_name.lower().capitalize()
        self.object_name_plural = f"{object_name}s"
        self.fetch_success = f"{self.object_name_plural} fetched successfully"
        self.fetch_fail = f"{self.object_name_plural} fetch failed"
        self.fetch_single_success = f"{self.object_name} fetched successfully"
        self.fetch_single_fail = f"{self.object_name} fetch failed"
        self.create_success = f"{self.object_name} created successfully"
        self.create_fail = f"{self.object_name} creation failed"
        self.update_success = f"{self.object_name} updated successfully"
        self.update_fail = f"{self.object_name} update failed"
        self.delete_success = f"{self.object_name} deleted successfully"
        self.delete_fail = f"{self.object_name} deletion failed"
        self.action_success = f"{self.object_name} action successful"
        self.action_fail = f"{self.object_name} action failed"
        self.not_found = f"{self.object_name} not found"
        self.already_exists = f"{self.object_name} already exists"
        self.invalid_data = f"Invalid {self.object_name} data"
        self.invalid_data_plural = f"Invalid {self.object_name_plural} data"
        self.invalid_data_single = f"Invalid {self.object_name} data"
        self.unauthorized = f"Unauthorized {self.object_name} action"
        self.forbidden = f"Forbidden {self.object_name} action"
        self.not_authenticated = "Not authenticated"
        self.upload_failed = f"{self.object_name} upload failed"
        self.missing_data = f"Missing {self.object_name} data"


class CRUDSummaryDescription:
    def __init__(self, object_name: str):
        self.object_name = object_name.lower().capitalize()
        self.object_name_plural = f"{object_name}s"
        self.fetch_summary = f"Get {self.object_name_plural}"
        self.fetch_description = f"Get {self.object_name_plural}"
        self.fetch_single_summary = f"Get {self.object_name}"
        self.fetch_single_description = f"Get {self.object_name}"
        self.create_summary = f"Create {self.object_name}"
        self.create_description = f"Create {self.object_name}"
        self.update_summary = f"Update {self.object_name}"
        self.update_description = f"Update {self.object_name}"
        self.partial_update_summary = f"Partial update {self.object_name}"
        self.partial_update_description = f"Partial update {self.object_name}"
        self.delete_summary = f"Delete {self.object_name}"
        self.delete_description = f"Delete {self.object_name}"
        self.action_summary = f"Action on {self.object_name}"
        self.action_description = f"Action on {self.object_name}"

    def get_action_summary(self, action_name: str):
        return f"{action_name} {self.object_name}"

    def get_action_description(self, action_name: str):
        return f"{action_name} {self.object_name}"


def response_error_schema_generator(
    service_name: str, response_messages: ResponseMessages
):
    not_found = ApiResponse[None](
        data=None, meta=MetaData(message=response_messages.not_found)
    ).model_dump_json()
    not_found = json.loads(not_found)
    conflict = ApiResponse[None](
        data=None, meta=MetaData(message=response_messages.already_exists)
    ).model_dump_json()
    conflict = json.loads(conflict)
    bad_request = ApiResponse[None](
        data=None, meta=MetaData(message=response_messages.invalid_data)
    ).model_dump_json()
    bad_request = json.loads(bad_request)
    forbidden = ApiResponse[None](
        data=None, meta=MetaData(message=response_messages.forbidden)
    ).model_dump_json()
    forbidden = json.loads(forbidden)
    unauthorized = ApiResponse[None](
        data=None, meta=MetaData(message=response_messages.unauthorized)
    ).model_dump_json()
    unauthorized = json.loads(unauthorized)
    content_type = "application/json"
    return {
        status.HTTP_404_NOT_FOUND: {"content": {content_type: {"example": not_found}}},
        status.HTTP_409_CONFLICT: {"content": {content_type: {"example": conflict}}},
        status.HTTP_400_BAD_REQUEST: {
            "content": {content_type: {"example": bad_request}}
        },
        status.HTTP_403_FORBIDDEN: {"content": {content_type: {"example": forbidden}}},
        status.HTTP_401_UNAUTHORIZED: {
            "content": {content_type: {"example": unauthorized}}
        },
    }
