import datetime

from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from AdNotifyManager.api.serializers import GoodsRequestSerializer
from AdNotifyManager.models import Goods


class GoodsView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.has_perm('AdNotifyManager.add_goods'):
            return Response({}, status=status.HTTP_403_FORBIDDEN)

        serialazer = GoodsRequestSerializer(data=request.data)
        if serialazer.is_valid(raise_exception=True):

            pk = self.request.data["external_id"]
            goods = Goods.objects.filter(external_id=pk).first()
            if goods is not None:
                return Response({"success": "Ok"}, status=status.HTTP_200_OK)

            data_create = datetime.datetime.now()
            goods = serialazer.save(data_create=data_create)
            return Response({"success": "Ok", "id": goods.id}, status=status.HTTP_201_CREATED)
