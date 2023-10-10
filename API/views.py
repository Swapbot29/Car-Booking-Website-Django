from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from ST_App.models import Car
from .serializers import CarSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Create your views here.

class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CarUpdateViews(generics.RetrieveUpdateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'pk'

class CarDetailView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser,IsAuthenticated]
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CreateAPIViews(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser,IsAuthenticated]
    def post(self,request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.data,status=status.HTTP_401_BAD_REQUEST)
    
class CarDeleteViews(APIView):
    def delete(self,request,id=None):
        car_data = Car.objects.filter(id=id)
        if car_data:
            car_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)