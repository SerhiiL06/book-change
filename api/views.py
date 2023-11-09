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


class BookRelationsAPIView(APIView):
    def get(self, request):
        queryset = BookRelations.objects.all()
        serilizer = BookRelationsSerializer(queryset, many=True)
        return Response({"relations": serilizer.data})

    def post(self, request):
        data = BookRelationsSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        book_relations = BookRelations(
            book=data.validated_data["book"],
            user=data.validated_data["user_id"],
            bookmark=data.validated_data["bookmark"],
            rating=data.validated_data["rating"],
        )
        if book_relations.exists():
            return Response({"wrong": "try another method!"})
        return Response({"well_done": data.data})


class DetailBookRelationsAPIView(APIView):
    def get(self, request, id):
        try:
            obj = BookRelations.objects.get(id=id)
        except:
            return Response({"wrong": "doesnotexist"})
        serializer = BookRelationsSerializer(obj, many=False)

        return Response({"obj": serializer.data})

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if not id:
            return Response({"error": "Dont work"})

        try:
            book_relations = BookRelations.objects.get(id=id)
        except:
            return Response({"error": "Dont work"})

        serializer = BookRelationsSerializer(data=request.data, instance=book_relations)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"update": serializer.data})

    def delete(self, request, id):
        obj = BookRelations.objects.get(id=id)
        # BookRelationsSerializer(obj, many=False)
        obj.delete()
        return Response({"delete": "OK"})
