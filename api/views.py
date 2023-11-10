from django_filters import rest_framework as filter
from rest_framework import filters, permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView


from book_relations.models import BookRelations
from book_relations.serializers import BookRelationsSerializer
from book_requests.models import BookRequest
from book_requests.serializers import BookRequestSerializer


class BookRequestAPIView(APIView):
    def get(self, *args, **kwargs):
        queryset = BookRequest.objects.all().values()
        serializer = BookRequestSerializer(queryset, many=True).data

        return Response({"list": serializer})

    def post(self, request):
        data = BookRequestSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        BookRequest.objects.create(
            book_id=data.validated_data["book_id"],
            request_from_user_id=data.validated_data["request_from_user_id"],
            comment=data.validated_data["comment"],
        )
        return Response({"OKEY": data.data})
