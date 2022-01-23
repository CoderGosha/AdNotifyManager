from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from AdNotifyManager.api.serializers import PingSerializer
from AdNotifyManager.extensions.http_extensions import visitor_ip_address
from AdNotifyManager.models import Node


class PingView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"Ok"})

    def post(self, request):
        serialazer = PingSerializer(data=request.data)
        ip_address = visitor_ip_address(request)
        if serialazer.is_valid(raise_exception=True):
            ping = Node.objects.filter(name=serialazer.validated_data['name']).first()
            if ping is None:
                ping = serialazer.save(owner=self.request.user, ip_address=ip_address)
            else:
                ping = serialazer.update(ping, validated_data=request.data)
                ping.ip_address = ip_address
                ping.save()
            return Response({"success": "Ok"})