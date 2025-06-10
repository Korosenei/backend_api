from rest_framework.response import Response
from rest_framework import status


class CustomResponse:
    @staticmethod
    def success(data=None, message="Opération réussie", status_code=status.HTTP_200_OK):
        return Response(
            {
                "httpCode": status_code,
                "message": message,
                "data": data,
            },
            status=status_code,
        )

    @staticmethod
    def error(message="Une erreur s'est produite", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "httpCode": status_code,
                "message": message,
                "errors": errors or [],
            },
            status=status_code,
        )
