from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import ClubSerializer
from .models import Club

# Create your views here.


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/player-list/',
        'Detail': '/player-detail/<str:pk>/',
        'Create': '/player-create/',
        'Update': '/player-update/<str:pk>/',
        'Delete': '/player-delete/<str:pk>/'
    }
    return Response(api_urls)


@api_view(['GET'])
def playerList(request):
    md = Club.objects.all()
    serializer = ClubSerializer(md, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def playerDetail(request, pk):
    md = Club.objects.get(id=pk)
    serializer = ClubSerializer(md, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def playerCreate(request):
    # manchester utd tu
    # sprint(request.data)
    data = Club.objects.all().values()
    mylist = []
    for i in data:
        bl = i["club"]
        mylist.append(bl)
    print(mylist)
    print("---tintest mitambo-------")
    for data in request.data:
        if (data["club"]) in mylist:
            Club.objects.update(position=data["first_name"])
        else:
            pass

    serializer = ClubSerializer(data=request.data)
    print("-----------------------------")
    print(serializer)
    if serializer.is_valid():
        pass
        # print(serializer.validated_data)
        # serializer.save()
    return Response(serializer.data)


########## CLASS BASED VIEWS ############
class PlayerListAPIView(APIView):
    def get(self, request):
        md = Club.objects.all()
        serializer = ClubSerializer(md, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClubSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerDetailAPIView(APIView):

    def get_object(self, id):
        try:
            return Club.objects.get(pk=id)
        except Club.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        serializer = ClubSerializer(self.get_object(id))
        return Response(serializer.data)

    def put(self, request, id):
        serializer = ClubSerializer(self.get_object(id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        ClubSerializer(self.get_object(id)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Generic Views and MiXins


class ClubModalViewset(viewsets.ModelViewSet):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()


class ClubViewset(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()


class GenericAPIView(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    lookup_field = 'id'
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)
