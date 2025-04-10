from typing import Generic, List

from .query import OffsetLimitQueryModel
from .typing import T


class StatusCodes:
    """
    StatusCodes class.
    This class contains the status codes used in the application.
    """

    BAD_REQUEST_400 = 400
    UNAUTHORIZED_401 = 401
    NOT_FOUND_404 = 404
    FORBIDDEN_403 = 403
    METHOD_NOT_ALLOWED_405 = 405
    CONFLICT_409 = 409
    UNPROCESSABLE_ENTITY_422 = 422

    CREATED_201 = 201
    OK_200 = 200
    NO_CONTENT_204 = 204

    INTERNAL_SERVER_ERROR_500 = 500


statusCodes = StatusCodes()


class OffsetLimitResponseModel(OffsetLimitQueryModel):
    """
    OffsetLimitResponseModel class.
    This is used for pagination response.
    """

    def response(self, object_list: List[T]) -> dict:
        """
        Return a dictionary with the object list and the offset and limit values.
        """
        return {
            "offset": 0,
            "limit": 2,
            "object_list": object_list,
        }


class ResponseListModel(OffsetLimitQueryModel, Generic[T]):
    object_list: List[T] = []
