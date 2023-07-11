from django.shortcuts import render
from rest_framework import generics

from carousel.models import CarouselModel, BannerADSModel
from carousel.serializers import CarouselModelSerializer, BannerADSModelSerializer


class CarouselModelAPIView(generics.ListAPIView):
    queryset = CarouselModel.objects.all()
    serializer_class = CarouselModelSerializer


class BannerADSModelAPIView(generics.ListAPIView):
    queryset = BannerADSModel.objects.all()
    serializer_class = BannerADSModelSerializer
