import coreapi
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.views import APIView


class TokenView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
            Создадим нового пользователя и вернем его токен + имя
        :param request:
        :return:
        """
        name = self.request.query_params.get('name')
        if name is None:
            return Response(f"Invalid name", status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=name).exists():
            return Response(f"User: {name} is use", status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=name)

        token = Token(user_id=user.id)
        token.save()

        return Response(f'Name: {name}, Token: {token.key}')

