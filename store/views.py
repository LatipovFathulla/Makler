from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from products.utils import get_wishlist_data
from .models import StoreModel, HowStoreServiceModel, UseForModel, StoreBrandModel
from rest_framework.response import Response
from .serializers import StoreModelSerializer, UpdateStoreModelSerializer, HowStoreServiceModelSerializer, \
    UseForModelSerializer, ALLStoreModelSerializer, StoreBrandModelSerializer, PatchStoreUpdateModelSerializer


class StoreModelAPIView(generics.ListAPIView):
    queryset = StoreModel.objects.order_by('-pk')
    serializer_class = ALLStoreModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['use_for', 'how_store_service', 'brand_title']


class StoreBrandAPIView(generics.ListAPIView):
    queryset = StoreBrandModel.objects.order_by('-pk')
    serializer_class = StoreBrandModelSerializer


class RandomStoreModelAPIView(generics.ListAPIView):
    queryset = StoreModel.objects.order_by('?')
    serializer_class = ALLStoreModelSerializer


class SearchStoreModelAPIView(generics.ListAPIView):
    queryset = StoreModel.objects.order_by('pk')
    serializer_class = StoreModelSerializer
    filter_backends = [SearchFilter]
    search_fields = ['address']


def add_to_wishlist(request, pk):
    try:
        product = StoreModel.objects.get(pk=pk)
    except StoreModel.DoesNotExist:
        return Response(data={'status': False})
    wishlist = request.session.get('wishlist', [])
    if product.pk in wishlist:
        wishlist.remove(product.pk)
        data = {'status': True, 'added': False}
    else:
        wishlist.append(product.pk)
        data = {'status': True, 'added': True}
    request.session['wishlist'] = wishlist

    data['wishlist_len'] = get_wishlist_data(wishlist)
    return JsonResponse(data)


class StoreDetailAPIView(APIView):
    def get(self, request, pk):
        houses = StoreModel.objects.get(id=pk)
        houses.view_count += 1
        houses.save()
        serializer = ALLStoreModelSerializer(houses, context={'request': request})
        return Response(serializer.data)


class StoreAddCreateAPIView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = StoreModelSerializer
    parser_classes = [MultiPartParser]
    queryset = StoreModel.objects.all()
    permission_classes = [IsAuthenticated, ]


class StoreUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = StoreModel.objects.all()
    serializer_class = UpdateStoreModelSerializer


class StorePatchUpdateAPIView(generics.UpdateAPIView):
    queryset = StoreModel.objects.all()
    serializer_class = PatchStoreUpdateModelSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['draft'] = True
        kwargs['product_status'] = 3
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class StoreDestroyAPIView(mixins.DestroyModelMixin, GenericViewSet):
    queryset = StoreModel.objects.all()
    serializer_class = StoreModelSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UseForModelSerializerAPIView(generics.ListAPIView):
    queryset = UseForModel.objects.all()
    serializer_class = UseForModelSerializer


class HowStoreServiceModelSerializerAPIView(generics.ListAPIView):
    queryset = HowStoreServiceModel.objects.all()
    serializer_class = HowStoreServiceModelSerializer
