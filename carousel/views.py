from django.shortcuts import render
from rest_framework import generics

from carousel.models import CarouselModel
from carousel.serializers import CarouselModelSerializer


class CarouselModelAPIView(generics.ListAPIView):
    queryset = CarouselModel.objects.all()
    serializer_class = CarouselModelSerializer
