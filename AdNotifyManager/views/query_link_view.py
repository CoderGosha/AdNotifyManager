from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from AdNotifyManager.api.serializers import QueryLinkItemSerializer
from AdNotifyManager.models import QueryLink, Node


class QueryLinkView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = self.request.query_params.get('name')

        if name is None:
            return Response(f"Invalid name", status.HTTP_400_BAD_REQUEST)
        node = Node.objects.filter(name=name).filter(owner=self.request.user).first()

        if node is None:
            return Response(f"Node not found", status.HTTP_404_NOT_FOUND)

        query_links = self.get_query_link(node.id)

        serializer = QueryLinkItemSerializer(query_links, many=True)
        return Response(serializer.data)

    def get_query_link(self, id):
        query_links = QueryLink.objects.filter(node__id=id).filter(subscriber__isnull=False).order_by('data_create').all()

        return query_links
