from rest_framework import serializers

from carousel.models import CarouselModel, BannerADSModel


class CarouselModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselModel
        fields = '__all__'


class BannerADSModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerADSModel
        fields = '__all__'
