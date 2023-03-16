from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication

from products.utils import get_wishlist_data
from user.models import CustomUser
from user.views import premium_required
from .models import MasterModel, MasterUserWishlistModel, MasterProfessionModel, HowServiceModel
from .serializers import MasterSerializer, MasterDetailSerializer, MasterCreateSerializer, \
    MasterGetUserWishlistModelSerializer, MasterUserWishlistModelSerializer, MasterProfessionSerializer, \
    APPMasterCreateSerializer, UpdSerializer, UpdMasterCreateSerializer, HowServiceModelSerializer


class MasterListAPIView(generics.ListAPIView):
    ''' Masters '''
    queryset = MasterModel.objects.order_by('pk')
    serializer_class = MasterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['profession', 'how_service']


class APPMasterListAPIView(generics.ListAPIView):
    ''' Masters '''
    queryset = MasterModel.objects.order_by('pk')
    serializer_class = MasterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['profession', 'how_service']


class RandomMasterListAPIView(generics.ListAPIView):
    ''' Masters '''
    queryset = MasterModel.objects.order_by('?')
    serializer_class = MasterSerializer


class SearchMasterListAPIView(generics.ListAPIView):
    ''' Masters '''
    queryset = MasterModel.objects.order_by('pk')
    serializer_class = MasterSerializer
    filter_backends = [SearchFilter]
    search_fields = ['address_title']


def add_to_wishlist(request, pk):
    try:
        product = MasterModel.objects.get(pk=pk)
    except MasterModel.DoesNotExist:
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


class MasterDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Получения Мастера(ID)",
        operation_description="Метод получения данных мастера. Помимо типа данных и токен авторизации, передаётся только ID мастера.",
    )
    def get(self, request, pk):
        products = MasterModel.objects.get(id=pk)
        products.view_count += 1
        products.save()
        serializer = MasterDetailSerializer(products, context={'request': request})
        return Response(serializer.data)


#
# class MasterAddCreateAPIView(mixins.CreateModelMixin, GenericViewSet):
#     queryset = MasterModel.objects.all()
#     serializer_class = MasterCreateSerializer
#
#     def get_serializer_context(self):
#         return {'request': self.request}


class MasterCreateAPIView(mixins.CreateModelMixin, GenericViewSet):
    queryset = MasterModel.objects.all()
    serializer_class = MasterCreateSerializer
    permission_classes = [IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     user = request.user
    #
    #     if not user.is_authenticated:
    #         return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    #
    #     if not user.is_premium:
    #         return Response({"error": "User is not premium"}, status=status.HTTP_403_FORBIDDEN)
    #
    #     data = request.data.copy()
    #     data["is_premium"] = user.is_premium
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

def premium_required(view_func):
    @login_required
    def _wrapped_view_func(request, *args, **kwargs):
        account = get_object_or_404(CustomUser, user=request.user)
        if not account.is_premium:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view_func


class MasterTestAPIView(APIView):
    def post(self, request):
        masters = MasterModel.objects.all()
        if masters.is_premium:
            serializer = MasterCreateSerializer(masters, context={'request': request})
            return Response(serializer.data)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

# APPMasterCreateSerializer
class APPMasterCreateAPIView(mixins.CreateModelMixin, GenericViewSet):
    queryset = MasterModel.objects.all()
    serializer_class = APPMasterCreateSerializer
    permission_classes = [IsAuthenticated, ]


    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #     data["is_premium"] = True
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        snippets = MasterModel.objects.all()
        serializer = MasterCreateSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MasterCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def get_object(self):
#     return MasterModel.objects.all()
#
# def get(self, request):
#     serailizer = self.serializer_class(self.get_object(), context={'request': request}, many=True)
#     return Response(serailizer.data, status=200)
#
# def post(self, request):
#     serializer = self.serializer_class(data=request.data)
#     if serializer.is_valid():
#         serializer.create(validated_data=serializer.validated_data, owner=request.user)
#     return Response(serializer.data)


class MasterUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = MasterModel.objects.all()
    serializer_class = UpdMasterCreateSerializer


class MasterPatchUpdateAPIView(generics.UpdateAPIView):
    queryset = MasterModel.objects.all()
    serializer_class = UpdSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['draft'] = True
        kwargs['product_status'] = 3
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class MasterDestroyAPIView(mixins.DestroyModelMixin, GenericViewSet):
    queryset = MasterModel.objects.all()
    serializer_class = MasterCreateSerializer

    @swagger_auto_schema(
        operation_summary="Удаления мастера(ID)",
        operation_description="Метод для удаления данных мастера. Помимо типа данных и токен авторизации, передаётся только ID мастера.",
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MasterUserWishlistModelView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin, GenericViewSet):
    queryset = MasterUserWishlistModel.objects.all()
    serializer_class = MasterUserWishlistModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


class GetMasterFavListAPIView(generics.ListAPIView):
    ''' Fav (Houses)'''
    queryset = MasterUserWishlistModel.objects.order_by('pk')
    serializer_class = MasterGetUserWishlistModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


class MasterProfessionListAPIView(generics.ListAPIView):
    queryset = MasterProfessionModel.objects.all()
    serializer_class = MasterProfessionSerializer


class MasterFiltersListAPIView(generics.ListAPIView):
    queryset = HowServiceModel.objects.all()
    serializer_class = HowServiceModelSerializer
