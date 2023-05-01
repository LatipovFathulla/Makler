from django.http import JsonResponse, HttpResponse
from django.utils import translation
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, DestroyAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import activate

from makler import settings
from masters.models import MasterModel
from masters.serializers import MasterSerializer
from mebel.models import MebelModel
from mebel.serializers import AllMebelSerializer
from store.models import StoreModel
from store.serializers import ProfileStoreModelSerializer
from user.models import CustomUser
from user.serializers import UserProductsSerializer
from .models import PriceListModel, UserWishlistModel, NewHouseImages
from rest_framework.decorators import api_view

from products.models import CategoryModel, HouseModel, AmenitiesModel
from products.serializers import CategorySerializer, HomeSerializer, AmenitiesSerializer, \
    HomeCreateSerializer, \
    WebAmenitiesSerializer, NewHomeCreateSerializer, WebPriceSerializer, NewWebHomeCreateSerializer, \
    NewAllWebHomeCreateSerializer, APPHomeCreateSerializer, UserWishlistModelSerializer, \
    GetUserWishlistModelSerializer, HomeUpdatePatchSerializer, HomeAddSerializer, ProductLinkSerializer, \
    HomeFilterNumberSerializer, HomeFilterObjectSerializer
from products.utils import get_wishlist_data


class CategoryListAPIView(generics.ListAPIView):
    ''' Categories '''
    queryset = CategoryModel.objects.order_by('pk')
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if language:
            activate(language)

        return super().list(request, *args, **kwargs)


class AmenitiesListAPIView(generics.ListAPIView):
    ''' Удобства (Amenities in product)'''
    queryset = AmenitiesModel.objects.order_by('pk')
    serializer_class = AmenitiesSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 1000


# web
class WebAmenitiesListAPIView(generics.ListAPIView):
    ''' web amenities '''
    queryset = AmenitiesModel.objects.order_by('-pk')
    serializer_class = WebAmenitiesSerializer


class WebPriceListAPIView(generics.ListAPIView):
    queryset = PriceListModel.objects.order_by('-pk')
    serializer_class = WebPriceSerializer
    pagination_class = StandardResultsSetPagination


class HouseListAPIView(generics.ListAPIView):
    ''' Products (Houses)'''
    queryset = HouseModel.objects.filter(draft=False)
    serializer_class = HomeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['number_of_rooms', 'price', 'address', 'category']
    pagination_class = StandardResultsSetPagination
    search_fields = ['title']


def add_to_wishlist(request, pk):
    try:
        product = HouseModel.objects.get(pk=pk)
    except HouseModel.DoesNotExist:
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


# web WebHomeSerializer
class WebHouseListAPIView(generics.ListAPIView):
    ''' Products (Houses)'''
    queryset = HouseModel.objects.filter(draft=False)
    serializer_class = NewWebHomeCreateSerializer


# web create Home

class WebHomeListAPIView(ListAPIView):
    queryset = HouseModel.objects.all()
    serializer_class = NewAllWebHomeCreateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_status', 'object', 'building_type', 'number_of_rooms',
                        'type', 'rental_type']

    search_fields = ['title', 'web_address_title']
    ordering_fields = ['id', 'price', 'created_at']

    def list(self, request, *args, **kwargs):
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if language:
            activate(language)

        return super().list(request, *args, **kwargs)

    # def get_queryset(self):
    #     queryset = self.queryset
    #     change_model_field.delay()
    #     return queryset


# class ArchiveProductListView(ListAPIView):
#     serializer_class = NewAllWebHomeCreateSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def get_queryset(self):
#         user_id = self.kwargs.get('user_id')
#         user = self.request.user
#         if user.is_authenticated:
#             return HouseModel.objects.filter(product_status=3, creator_id=user_id)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

class ArchiveProductListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        houses = HouseModel.objects.filter(creator_id=user, product_status=3)
        stores = StoreModel.objects.filter(creator_id=user, product_status=3)
        masters = MasterModel.objects.filter(owner_id=user, product_status=3)
        mebels = MebelModel.objects.filter(creator_id=user, product_status=3)

        houses_serializer = NewAllWebHomeCreateSerializer(houses, many=True, context={'request': request})
        stores_serializer = ProfileStoreModelSerializer(stores, many=True, context={'request': request})
        masters_serializer = MasterSerializer(masters, many=True, context={'request': request})
        mebels_serializer = AllMebelSerializer(mebels, many=True, context={'request': request})

        response_data = {
            'houses': houses_serializer.data,
            'stores': stores_serializer.data,
            'masters': masters_serializer.data,
            'mebels': mebels_serializer.data,
        }

        return Response(response_data)


# class ArchiveProductListView(generics.ListAPIView):
#     serializer_class = NewAllWebHomeCreateSerializer
#     permission_classes = [IsAuthenticated, ]
#
#     def get_queryset(self):
#         user = self.request.user
#         return HouseModel.objects.filter(product_status=3, creator=user)
# def get(self, request, *args, **kwargs):
#     houses = HouseModel.objects.filter(product_status=3)
#     maklers = MasterModel.objects.filter(product_status=3)
#     stores = StoreModel.objects.filter(product_status=3)
#     mebels = MebelModel.objects.filter(product_status=3)
#
#     serialized_data = UserProductsSerializer({
#         'houses': houses,
#         'maklers': maklers,
#         'stores': stores,
#         'mebels': mebels,
#     }, context={'request': request})
#
#     return Response(serialized_data.data)
# def get_queryset(self):
#     return HouseModel.objects.filter(product_status=3)


class SearchWebHomeListAPIView(ListAPIView):
    queryset = HouseModel.objects.all()
    serializer_class = NewAllWebHomeCreateSerializer
    filter_backends = [SearchFilter]
    search_fields = ['web_address_title']


class WebHomeCreateView(mixins.CreateModelMixin, GenericViewSet):
    queryset = HouseModel.objects.all()
    serializer_class = NewWebHomeCreateSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated, ]

    # def create(self, validated_data):
    #     targetDef = validated_data.pop(targetDefn)
    #
    #
    #     #save the objects into its respective models.
    #     targetDefId = TargetDefination.objects.create(**targetDef)
    #
    #     #get the objects of roleId and empID
    #     role = list(validated_data['roleId'].items())
    #     role_id = Role.objects.get(roleName =role[0][1])
    #     emp_id = Employee.objects.get(pk=validated_data['empId']['id'])
    #
    #     target_obj = Target.object.create(targetDef=targetDefId, roleId=role_id, empID=emp_id, startDate=validated_data['startDate'], endDate=validated_data['endDate'], value=validated_data['value'])
    #
    #     return target_obj

    # def create(self, validated_data):
    #

    # uv = PriceListModel(price=str(request.data['price_type']))
    # serializer = self.serializer_class(uv, data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# web
@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        snippets = HouseModel.objects.all()
        serializer = NewWebHomeCreateSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NewWebHomeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def add_to_wishlist(request, pk):
    try:
        product = HouseModel.objects.get(pk=pk)
    except HouseModel.DoesNotExist:
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


class HouseDetailAPIView(APIView):
    def get(self, request, pk):
        houses = HouseModel.objects.get(id=pk)
        houses.view_count += 1
        houses.save()
        serializer = NewAllWebHomeCreateSerializer(houses, context={'request': request}, )
        return Response(serializer.data)


class WishlistHouseDetailAPIView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = HouseModel.objects.all()
    serializer_class = NewWebHomeCreateSerializer

    def update(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class HouseAddCreateAPIView(generics.CreateAPIView):
    queryset = HouseModel.objects.all()
    serializer_class = NewHomeCreateSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        return {'request': self.request}


class APPHouseAddCreateAPIView(generics.CreateAPIView):
    queryset = HouseModel.objects.all()
    serializer_class = APPHomeCreateSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        return {'request': self.request}


class HouseUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = HouseModel.objects.all()
    serializer_class = NewWebHomeCreateSerializer

    def update(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PatchHouseUpdateAPIView(generics.UpdateAPIView):
    queryset = HouseModel.objects.all()
    serializer_class = HomeUpdatePatchSerializer
    permission_classes = [IsAuthenticated, ]

    def partial_update(self, request, *args, **kwargs):
        kwargs['draft'] = True
        kwargs['product_status'] = 3
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class AddWishlistHousePIView(generics.UpdateAPIView):
    queryset = HouseModel.objects.all()
    serializer_class = HomeAddSerializer
    permission_classes = [IsAuthenticated, ]

    def partial_update(self, request, *args, **kwargs):
        isBookmarked = request.data.get('isBookmarked', False)
        kwargs['isBookmarked'] = isBookmarked
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class HouseDestroyAPIView(mixins.DestroyModelMixin, GenericViewSet):
    queryset = HouseModel.objects.all()
    serializer_class = HomeCreateSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserWishlistModelView(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin, GenericViewSet):
    queryset = UserWishlistModel.objects.all()
    serializer_class = UserWishlistModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


# class UserWishlistDeleteView(mixins.DestroyModelMixin, GenericViewSet):
#     queryset = UserWishlistModel.objects.all()
#     serializer_class = UserWishlistModelSerializer
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class WishlistUserHouseDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        houses = HouseModel.objects.filter(creator_id=user, isBookmarked=True)
        stores = StoreModel.objects.filter(creator_id=user, isBookmarked=True)
        masters = MasterModel.objects.filter(owner_id=user, isBookmarked=True)
        mebels = MebelModel.objects.filter(creator_id=user, isBookmarked=True)

        houses_serializer = NewAllWebHomeCreateSerializer(houses, many=True, context={'request': request})
        stores_serializer = ProfileStoreModelSerializer(stores, many=True, context={'request': request})
        masters_serializer = MasterSerializer(masters, many=True, context={'request': request})
        mebels_serializer = AllMebelSerializer(mebels, many=True, context={'request': request})

        response_data = {
            'houses': houses_serializer.data,
            'stores': stores_serializer.data,
            'masters': masters_serializer.data,
            'mebels': mebels_serializer.data,
        }

        return Response(response_data)

    # def get_queryset(self, *args, **kwargs):
    #     return (
    #         super()
    #             .get_queryset(*args, **kwargs)
    #             .filter(user_id=self.kwargs.get('pk'))
    #     )

    # def get(self, request, pk):
    #     # pk = self.kwargs.get("pk")
    #     houses = UserWishlistModel.objects.filter(user_id=pk)
    #     serializer = UserWishlistModelSerializer(houses, many=True)
    #     return Response(serializer.data)

    # def delete(self, request, pk):


class GetHouseFavListAPIView(generics.ListAPIView):
    ''' Fav (Houses)'''
    queryset = UserWishlistModel.objects.order_by('pk')
    serializer_class = GetUserWishlistModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']


class RandomHouseModelAPIView(generics.ListAPIView):
    queryset = HouseModel.objects.order_by('?')
    serializer_class = NewAllWebHomeCreateSerializer


class HouseImageDestroyView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = NewHouseImages.objects.all()

    def destroy(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        image_id = self.kwargs.get('image_id')
        image_url = self.request.data.get('image_url')

        # get the image instance
        image = get_object_or_404(NewHouseImages, id=image_id, product_id=product_id)

        # delete the image from the storage
        storage, path = image.images.storage, image.images.path
        storage.delete(path)

        # delete the image instance from the database
        image.delete()

        return Response({'detail': 'Image deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class HomeFilterNumberView(ListAPIView):
    queryset = HouseModel.objects.all()
    serializer_class = HomeFilterNumberSerializer


# HomeFilterObjectSerializer
class HomeFilterObjectView(ListAPIView):
    queryset = HouseModel.objects.all()
    serializer_class = HomeFilterObjectSerializer
