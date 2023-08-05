from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from mebel.models import MebelCategoryModel, MebelModel
from mebel.serializers import MebelCategorySerializer, MebelSerializer, AllMebelSerializer, UpdateAllMebelSerializer, \
    PatchUpdateAllMebelSerializer


class MebelCategoryListAPIView(generics.ListAPIView):
    queryset = MebelCategoryModel.objects.order_by('pk')
    serializer_class = MebelCategorySerializer


class MebelListAPIView(ListAPIView):
    queryset = MebelModel.objects.order_by('pk')
    serializer_class = AllMebelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'web_address_title']

    def get_queryset(self):
        # Фильтруем продукты по product_status = 1 ('PUBLISH')
        return MebelModel.objects.filter(product_status=1)

class RandomMebelListAPIView(generics.ListAPIView):
    queryset = MebelModel.objects.order_by('?')
    serializer_class = AllMebelSerializer


class MebelCreateAPIView(mixins.CreateModelMixin, GenericViewSet):
    queryset = MebelModel.objects.all()
    serializer_class = MebelSerializer
    permission_classes = [IsAuthenticated, ]

    # def create(self, request, *args, **kwargs):
    #     user = request.user
    #
    #     if not user.is_authenticated:
    #         return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    #
    #     if not user.is_premium:
    #         return Response({"error": "User is not premium, to make it work, go to the admin panel and check the is_premium box for your user"}, status=status.HTTP_403_FORBIDDEN)
    #
    #     data = request.data.copy()
    #     data["is_premium"] = user.is_premium
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MebelUpdateView(generics.RetrieveUpdateAPIView):
    queryset = MebelModel.objects.all()
    serializer_class = UpdateAllMebelSerializer


class PatchMebelUpdateView(generics.RetrieveUpdateAPIView):
    queryset = MebelModel.objects.all()
    serializer_class = PatchUpdateAllMebelSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['draft'] = True
        kwargs['product_status'] = 3
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class MebelDetailAPIView(APIView):
    def get(self, request, pk):
        products = MebelModel.objects.get(id=pk)
        products.view_count += 1
        products.save()
        serializer = AllMebelSerializer(products, context={'request': request})
        return Response(serializer.data)


class MebelDestroyAPIView(mixins.DestroyModelMixin, GenericViewSet):
    queryset = MebelModel.objects.all()
    serializer_class = MebelSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
