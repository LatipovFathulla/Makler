from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import action

from masters.serializers import MasterSerializer
from products.helpers import modify_input_for_multiple_files
from products.models import CategoryModel, HouseModel, AmenitiesModel, MapModel, HouseImageModel, ImagesModel, \
    NewHouseImages, PriceListModel, HowSaleModel, UserWishlistModel
from store.serializers import StoreModelSerializer
from user.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'title', 'subtitle', 'image', 'created_at']


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenitiesModel
        fields = ['id', 'title', 'image', 'created_at']


# web
class WebAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenitiesModel
        fields = ['id', 'title', 'image', 'created_at']


class WebPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceListModel
        fields = ['id', 'price_t']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapModel
        exclude = ['created_at']


class HomeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImageModel
        fields = ['property_id', 'image']

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


# class ImagesModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model =
# class ImageSerializer(serializers.Serializer):
#     image = serializers.FileField(use_url=True)
#
#
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewHouseImages
        fields = ['images']

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_url(obj.image.url)


class APPHomeCreateSerializer(serializers.ModelSerializer):
    # address = AddressSerializer()
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = HouseModel
        fields = ['id', 'creator', 'title', 'descriptions', 'price', 'phone_number', 'app_currency', 'app_type',
                  'typeOfRent',
                  'typeOfHouse', 'rental_type', 'property_type',
                  'typeOfObject', 'app_ipoteka', 'app_mebel', 'type', 'web_address_title', 'web_address_latitude',
                  'web_address_longtitude', 'general', 'residential',
                  'number_of_rooms', 'floor', 'floor_from', 'building_type', 'amenities', 'youtube_link',
                  'images', 'uploaded_images', 'isBookmarked', 'draft', 'created_at',
                  ]
        extra_kwargs = {"creator": {"read_only": True}, "product_status": {"read_only": True}}

    def create(self, validated_data):
        title = validated_data.get('title')
        descriptions = validated_data.get('descriptions')
        price = validated_data.get('price')
        phone_number = validated_data.get('phone_number')
        app_currency = validated_data.get('app_currency')
        app_type = validated_data.get('app_type')
        typeOfRent = validated_data.get('typeOfRent')
        typeOfHouse = validated_data.get('typeOfHouse')
        typeOfObject = validated_data.get('typeOfObject')
        app_ipoteka = validated_data.get('app_ipoteka')
        app_mebel = validated_data.get('app_mebel')
        rental_type = validated_data.get('rental_type')
        property_type = validated_data.get('property_type')
        type = validated_data.get('type')
        web_address_title = validated_data.get('web_address_title')
        web_address_latitude = validated_data.get('web_address_latitude')
        web_address_longtitude = validated_data.get('web_address_longtitude')
        general = validated_data.get('general')
        residential = validated_data.get('residential')
        number_of_rooms = validated_data.get('number_of_rooms')
        floor = validated_data.get('floor')
        floor_from = validated_data.get('floor_from')
        building_type = validated_data.get('building_type')
        uploaded_datas = validated_data.pop('uploaded_images')
        youtube_link = validated_data.get('youtube_link')
        creator = self.context['request'].user
        amenities = validated_data.get('amenities')
        titles = [i.title for i in amenities]
        amenities_titles = AmenitiesModel.objects.filter(title__in=titles)
        new_product = HouseModel.objects.create(
            title=title,
            creator=creator,
            descriptions=descriptions,
            price=price,
            phone_number=phone_number,
            app_currency=app_currency,
            app_type=app_type,
            typeOfRent=typeOfRent,
            typeOfHouse=typeOfHouse,
            typeOfObject=typeOfObject,
            app_ipoteka=app_ipoteka,
            app_mebel=app_mebel,
            type=type,
            rental_type=rental_type,
            property_type=property_type,
            web_address_title=web_address_title,
            web_address_latitude=web_address_latitude,
            web_address_longtitude=web_address_longtitude,
            general=general,
            residential=residential,
            number_of_rooms=number_of_rooms,
            floor=floor,
            youtube_link=youtube_link,
            floor_from=floor_from,
            building_type=building_type,
        )
        new_product.amenities.add(*amenities_titles)
        for q in uploaded_datas:
            new_product_image = NewHouseImages.objects.create(product=new_product, images=q)
        return new_product

    def get_img_url(self, obj):
        urls = []
        for i in obj.images.all():
            myurl = self.context['request'].build_absolute_uri(i.image.url)
            urls.append(myurl)
        return urls


class NewHomeCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    # address = AddressSerializer()

    class Meta:
        model = HouseModel
        fields = ('title', 'descriptions', 'price', 'residential', 'number_of_rooms', 'phone_number',
                  'floor', 'floor_from', 'general', 'web_type', 'web_rental_type', 'object', 'web_building_type',
                  'isBookmarked',
                  'images', 'uploaded_images',)
        # extra_kwargs = {"user": {"read_only": True}}

    def get_img_url(self, obj):
        urls = []
        for i in obj.images.all():
            myurl = self.context['request'].build_absolute_uri(i.image.url)
            urls.append(myurl)
        return urls

    # def save(self, **kwargs):
    #     kwargs["creator"] = self.fields["creator"].get_default()
    #     return super().save(**kwargs)

    # def to_representation(self, instance):
    #     context = super().to_representation(instance)
    #     context['images'] = ImageSerializer(instance.images, many=True).data
    #     return context


class HomeCreateSerializer(serializers.ModelSerializer):
    images = serializers.FileField()

    class Meta:
        model = ImagesModel
        fields = ['image', ]

    class Meta:
        model = HouseModel
        fields = ['title', 'descriptions', 'price', 'address',
                  'residential', 'number_of_rooms', 'floor', 'floor_from', 'general', 'isBookmarked',
                  'images']
        extra_kwargs = {
            'images': {'required': False}
        }

    def to_representation(self, instance):
        context = super().to_representation(instance)
        # context['amenities'] = AmenitiesSerializer(instance.amenities, many=True).data
        # context['images'] = ImageSerializer(instance.images, many=True).data
        # context['category'] = CategorySerializer(instance.category).data
        context['address'] = AddressSerializer(instance.address).data
        return context

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_url(obj.image.url)
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get("title", instance.title)
    #     instance.descriptions = validated_data.get("descriptions", instance.descriptions)
    #     instance.price = validated_data.get("price", instance.price)
    #     instance.general = validated_data.get("general", instance.general)
    #     instance.residential = validated_data.get("residential", instance.residential)
    #     instance.number_of_rooms = validated_data.get("number_of_rooms", instance.number_of_rooms)
    #     instance.floor = validated_data.get("floor", instance.floor)
    #     instance.floor_from = validated_data.get("floor_from", instance.floor_from)
    #     # instance.image = validated_data.get("image", instance.image)
    #     instance.save()
    #     return instance


#  bu homeniki
class HomeSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    # address = AddressSerializer()
    # image = HomeImageSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = HouseModel
        fields = ['id', 'title', 'category', 'descriptions', 'price', 'phone_number', 'app_currency', 'app_type',
                  'typeOfRent',
                  'typeOfHouse', 'web_address_title', 'web_address_latitude', 'web_address_longtitude', 'rental_type',
                  'typeOfObject', 'app_ipoteka', 'app_mebel', 'type', 'address', 'general', 'residential',
                  'number_of_rooms', 'floor', 'floor_from', 'building_type', 'amenities', 'product_status',
                  'isBookmarked',
                  'images', 'uploaded_images', 'creator']


class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceListModel
        fields = ['price_t']


class NewWebHowSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowSaleModel
        fields = ['title']


class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel
        fields = ['type']


class HouseRentalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel
        fields = ['rental_type']


# web
class NewAllWebHomeCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    amenities = WebAmenitiesSerializer(many=True)
    price_type = PriceListSerializer()
    how_sale = NewWebHowSaleSerializer()
    type = HouseTypeSerializer

    # rental_type = HouseRentalTypeSerializer

    # address = AddressSerializer()

    class Meta:
        model = HouseModel
        fields = ['id', 'creator', 'title', 'descriptions', 'price', 'price_type',
                  'type', 'rental_type', 'property_type', 'object',
                  'web_address_title', 'web_address_latitude', 'web_address_longtitude',
                  'pm_general', 'pm_residential', 'images', 'uploaded_images',
                  'number_of_rooms', 'floor', 'floor_from', 'building_type',
                  'typeOfRent', 'typeOfHouse', 'typeOfObject',
                  'app_ipoteka', 'app_mebel', 'app_new_building',
                  'amenities', 'phone_number', 'youtube_link', 'how_sale',
                  'isBookmarked', 'draft', 'product_status', 'view_count', 'created_at',
                  ]


class HomeUpdatePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel
        fields = ['id', 'draft', 'creator', 'product_status']

        extra_kwargs = {"creator": {"read_only": True}}


class NewWebHomeCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    how_sale = NewWebHowSaleSerializer

    # address = AddressSerializer()

    class Meta:
        model = HouseModel
        fields = ['id', 'creator', 'title', 'descriptions', 'price', 'price_type',
                  'type', 'rental_type', 'property_type', 'object',
                  'web_address_title', 'web_address_latitude', 'web_address_longtitude',
                  'pm_general', 'pm_residential', 'images', 'uploaded_images',
                  'number_of_rooms', 'floor', 'floor_from', 'building_type',
                  'app_ipoteka', 'app_mebel', 'app_new_building',
                  'amenities', 'phone_number', 'how_sale', 'youtube_link',
                  'isBookmarked', 'draft', 'product_status', 'created_at',
                  ]
        extra_kwargs = {"creator": {"read_only": True}, "product_status": {"read_only": True}}

    def create(self, validated_data):
        title = validated_data.get('title')
        descriptions = validated_data.get('descriptions')
        price = validated_data.get('price')
        price_types = validated_data.pop('price_type')
        type = validated_data.get('type')
        how_sale = validated_data.get('how_sale')
        rental_type = validated_data.get('rental_type')
        property_type = validated_data.get('property_type')
        object = validated_data.get('object')
        web_address_title = validated_data.get('web_address_title')
        web_address_latitude = validated_data.get('web_address_latitude')
        web_address_longtitude = validated_data.get('web_address_longtitude')
        pm_general = validated_data.get('pm_general')
        pm_residential = validated_data.get('pm_residential')
        pm_kitchen = validated_data.get('pm_kitchen')
        number_of_rooms = validated_data.get('number_of_rooms')
        floor = validated_data.get('floor')
        floor_from = validated_data.get('floor_from')
        building_type = validated_data.get('building_type')
        app_ipoteka = validated_data.get('app_ipoteka')
        app_mebel = validated_data.get('app_mebel')
        app_new_building = validated_data.get('app_new_building')
        amenities = validated_data.get('amenities')
        phone_number = validated_data.get('phone_number')
        draft = validated_data.get('draft')
        isBookmarked = validated_data.get('isBookmarked')
        youtube_link = validated_data.get('youtube_link')
        uploaded_data = validated_data.pop('uploaded_images')
        creator = self.context['request'].user
        titles = [i.title for i in amenities]
        amenities_titles = AmenitiesModel.objects.filter(title__in=titles)
        price_t = PriceListModel.objects.get(price_t=price_types)
        target_objs = HouseModel.objects.create(price_type=price_t, creator=creator,
                                                title=title, price=price,
                                                how_sale=how_sale,
                                                web_address_title=web_address_title,
                                                phone_number=phone_number,
                                                web_address_latitude=web_address_latitude,
                                                web_address_longtitude=web_address_longtitude,
                                                type=type,
                                                draft=draft,
                                                isBookmarked=isBookmarked,
                                                rental_type=rental_type,
                                                object=object,
                                                descriptions=descriptions,
                                                property_type=property_type,
                                                pm_general=pm_general,
                                                pm_residential=pm_residential,
                                                pm_kitchen=pm_kitchen,
                                                number_of_rooms=number_of_rooms,
                                                floor=floor,
                                                youtube_link=youtube_link,
                                                floor_from=floor_from,
                                                building_type=building_type,
                                                app_ipoteka=app_ipoteka,
                                                app_mebel=app_mebel,
                                                app_new_building=app_new_building,
                                                )
        target_objs.amenities.add(*amenities_titles)
        # if creator in validated_data:
        # target_objs.creator.add(*creator)
        for uploaded_item in uploaded_data:
            new_product_image = NewHouseImages.objects.create(product=target_objs, images=uploaded_item)
        return target_objs

    def get_img_url(self, obj):
        urls = []
        for i in obj.images.all():
            myurl = self.context['request'].build_absolute_uri(i.image.url)
            urls.append(myurl)
        return urls


class HomeFavSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = HouseModel
        fields = ['id', 'title', 'price', 'address', 'isBookmarked', 'created_at']


class HomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['title']


class HomeDetailSerializer(serializers.ModelSerializer):
    category = HomeCategorySerializer()
    address = AddressSerializer()
    # image = HomeImageSerializer(many=True)
    amenities = AmenitiesSerializer(many=True)

    # choices = serializers.SerializerMethodField('get_choices')

    class Meta:
        model = HouseModel
        fields = '__all__'


class UserWishlistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWishlistModel
        fields = ['id', 'user', 'product']


class GetUserWishlistModelSerializer(serializers.ModelSerializer):
    product = NewAllWebHomeCreateSerializer()

    class Meta:
        model = UserWishlistModel
        fields = '__all__'

