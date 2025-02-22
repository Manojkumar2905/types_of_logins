
from constants.common_imports import *


class ResponseUtil:
    @staticmethod
    def success_response(data: Any = None, message: str = "Operation successful") -> Dict[str, Any]:
        return {
            "status": "success",
            "message": message,
            "data": data
        }

    @staticmethod
    def failure_response(error: str, message: Optional[str] = "An error occurred") -> Dict[str, Any]:
        result = {
            "status": "failure",
            "message": message,
            "error": error
        }

        return result
