from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers.user_login_serializer import UserLoginSerializer


class UserLoginViewSet(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    http_method_names = ["post"]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            "success": "True",
            "status code": status.HTTP_200_OK,
            "message": "User logged in  successfully",
            "email": serializer.data["email"],
            "token": "Bearer " + serializer.data["token"],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
