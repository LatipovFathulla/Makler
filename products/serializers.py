from rest_framework import serializers
from modeltranslation.utils import get_language
import os

from makler import settings
from products.models import CategoryModel, HouseModel, AmenitiesModel, HouseImageModel, ImagesModel, \
    NewHouseImages, PriceListModel, HowSaleModel, UserWishlistModel, Complaint, ComplaintModel


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    subtitle = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.title if get_language() == 'ru' else getattr(obj, f'title_{get_language()}')

    def get_subtitle(self, obj):
        return obj.subtitle if get_language() == 'ru' else getattr(obj, f'subtitle_{get_language()}')

    class Meta:
        model = CategoryModel
        fields = ['id', 'title', 'subtitle', 'image', 'created_at']


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenitiesModel
        fields = ['id', 'title', 'image', 'created_at']

    def get_title(self, obj):
        return obj.title if get_language() == 'ru' else getattr(obj, f'title_{get_language()}')


# web
class WebAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenitiesModel
        fields = ['id', 'title', 'image', 'created_at']


class WebPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceListModel
        fields = ['id', 'price_t']


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
        fields = ['id', 'images']

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_url(obj.image.url)


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintModel
        fields = ['pk', 'reasons']


class ComplaintCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    reason_id = serializers.IntegerField(required=False)
    other_reason = serializers.CharField(required=False)

    class Meta:
        model = Complaint
        fields = ['pk', 'reason', 'user', 'product']

    def create(self, validated_data):
        reason_id = validated_data.get('reason_id')
        other_reason = validated_data.get('other_reason')
        user = self.context['request'].user
        product_id = validated_data.get('product_id')
        product = HouseModel.objects.get(pk=product_id)

        if reason_id:
            try:
                reason = ComplaintModel.objects.get(pk=reason_id)
            except ComplaintModel.DoesNotExist:
                raise serializers.ValidationError('Invalid reason_id')
        elif other_reason:
            # Создаем экземпляр ComplaintModel для other_reason
            reason = Complaint.objects.create(other_reason=other_reason)
        else:
            raise serializers.ValidationError('You must provide either reason_id or other_reason.')

        # Создаем экземпляр Complaint с учетом reason или other_reason
        complaint = Complaint.objects.create(reason=reason if reason_id else None, user=user, product=product,
                                             other_reason=other_reason)
        return complaint


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

    def get_title(self, obj):
        return obj.title if get_language() == 'ru' else getattr(obj, f'title_{get_language()}')


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
    # type = HouseTypeSerializer
    type = serializers.SerializerMethodField()
    rental_type = serializers.SerializerMethodField()
    property_type = serializers.SerializerMethodField()
    object = serializers.SerializerMethodField()
    building_type = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    descriptions = serializers.SerializerMethodField()

    # rental_type = HouseRentalTypeSerializer

    def get_title(self, obj):
        return obj.title if get_language() == 'ru' else getattr(obj, f'title_{get_language()}')

    def get_descriptions(self, obj):
        return obj.descriptions if get_language() == 'ru' else getattr(obj, f'descriptions_{get_language()}')

    def get_type(self, obj):
        request = self.context.get('request')
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')  # Получаем значение accept-language
        type_mapping = {
            'uz': {
                'купить': 'Xarid qilish',  # Перевод для "купить" на узбекском языке
                'продать': 'Sotish',  # Перевод для "купить" на узбекском языке
                'аденда': 'Ijaraga berish',  # Перевод для "аренда" на узбекском языке
            },
            'ru': {
                'купить': 'Купить',  # Перевод для "купить" на русском языке
                'продать': 'Продать',  # Перевод для "купить" на русском языке
                'аденда': 'Аренда',  # Перевод для "аренда" на русском языке
            },
        }

        # Определите соответствие Accept-Language и значения type
        type_translations = type_mapping.get(accept_language, {})
        return type_translations.get(obj.type, obj.type)

    def get_rental_type(self, obj):
        request = self.context.get('request')
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')  # Получаем значение accept-language
        rental_type_mapping = {
            'uz': {
                'длительно': 'Uzoq mudatga',  # Перевод для "купить" на узбекском языке
                'несколько месяцев': 'Bir necha oy',  # Перевод для "купить" на узбекском языке
                'посуточно': 'Kunbay',  # Перевод для "аренда" на узбекском языке
            },
            'ru': {
                'длительно': 'Длительно',  # Перевод для "купить" на русском языке
                'несколько месяцев': 'Несколько месяце',  # Перевод для "купить" на русском языке
                'посуточно': 'Посуточно',  # Перевод для "аренда" на русском языке
            },
        }

        # Определите соответствие Accept-Language и значения type
        rental_type_translations = rental_type_mapping.get(accept_language, {})
        return rental_type_translations.get(obj.rental_type, obj.rental_type)

    def get_property_type(self, obj):
        request = self.context.get('request')
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')  # Получаем значение accept-language
        property_type_mapping = {
            'uz': {
                'жилая': 'yashash joyi',  # Перевод для "купить" на узбекском языке
                'коммерческая': 'kochmas mulk',  # Перевод для "купить" на узбекском языке
            },
            'ru': {
                'жилая': 'жилая',  # Перевод для "купить" на русском языке
                'коммерческая': 'коммерческая',  # Перевод для "купить" на русском языке
            },
        }

        # Определите соответствие Accept-Language и значения type
        get_property_type_translations = property_type_mapping.get(accept_language, {})
        return get_property_type_translations.get(obj.property_type, obj.property_type)

    def get_object(self, obj):
        request = self.context.get('request')
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')  # Получаем значение accept-language
        object_type_mapping = {
            'uz': {
                'квартира': 'kvartira',  # Перевод для "квартира" на узбекском языке
                'комната': 'hona',  # Перевод для "комната" на узбекском языке
                'дача': 'dacha',  # Перевод для "дача" на узбекском языке
                'дома': 'domlar',  # Перевод для "дома" на узбекском языке
                'участка': 'uchastka',  # Перевод для "участка" на узбекском языке
                'таунхаус': 'Taunhaus',  # Перевод для "таунхаус" на узбекском языке
                'спальное': 'Uhlash uchun',  # Перевод для "спальное" на узбекском языке
            },
            'ru': {
                'квартира': 'квартира',  # Перевод для "квартира" на русском языке
                'комната': 'комната',  # Перевод для "комната" на русском языке
                'дача': 'дача',  # Перевод для "дача" на русском языке
                'дома': 'дома',  # Перевод для "дома" на русском языке
                'участка': 'участка',  # Перевод для "участка" на русском языке
                'таунхаус': 'Townhouse',  # Перевод для "таунхаус" на русском языке
                'спальное': 'Bed_space',  # Перевод для "спальное" на русском языке
            },
        }

        # Определите соответствие Accept-Language и значения object
        object_type_translations = object_type_mapping.get(accept_language, {})
        return object_type_translations.get(obj.object, obj.object)

    def get_building_type(self, obj):
        request = self.context.get('request')
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')  # Получаем значение accept-language
        building_type_mapping = {
            'uz': {
                'кирпич': 'gisht',  # Перевод для "квартира" на русском языке
                'монолит': 'monolit',  # Перевод для "комната" на русском языке
                'панель': 'panel',  # Перевод для "дача" на русском языке
                'блочный': 'blok',  # Перевод для "дома" на русском языке
            },
            'ru': {
                'кирпич': 'кирпич',  # Перевод для "квартира" на русском языке
                'монолит': 'монолит',  # Перевод для "комната" на русском языке
                'панель': 'панель',  # Перевод для "дача" на русском языке
                'блочный': 'блочный',  # Перевод для "дома" на русском языке
            },
        }

        # Определите соответствие Accept-Language и значения object
        building_type_translations = building_type_mapping.get(accept_language, {})
        return building_type_translations.get(obj.building_type, obj.building_type)

    class Meta:
        model = HouseModel
        fields = ['id', 'creator', 'title', 'descriptions', 'price', 'price_type',
                  'type', 'rental_type', 'property_type', 'object',
                  'web_address_title', 'web_address_latitude', 'web_address_longtitude',
                  'pm_general', 'pm_residential', 'images', 'uploaded_images',
                  'number_of_rooms', 'floor', 'floor_from', 'building_type',
                  'app_ipoteka', 'app_mebel', 'app_new_building',
                  'amenities', 'phone_number', 'youtube_link', 'how_sale', 'link',
                  'isBookmarked', 'draft', 'product_status', 'view_count', 'created_at',
                  ]

    def get_link(self, obj):
        return "https://makler-uz.uz/"

    localized_fields = ['title', 'descriptions']

    def get_localized_field(self, obj, field_name):
        return getattr(obj, f'{field_name}_{get_language()}') if get_language() != 'ru' else getattr(obj, field_name)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field_name in self.localized_fields:
            ret[field_name] = self.get_localized_field(instance, field_name)
        ret['link'] = self.get_link(instance)
        return ret


class HomeImageDeleteSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.CharField(max_length=1000, write_only=True)
    # other fields

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HouseModel
        fields = ['id', 'images', 'uploaded_images', 'image_url']

    def get_image_url(self, obj):
        if obj.images.exists():
            return self.context['request'].build_absolute_uri(obj.images.first().images.url)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        image_url = request.data.get('uploaded_images')
        image_name = os.path.basename(image_url)
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        if os.path.exists(image_path):
            os.remove(image_path)
        return super().destroy(request, *args, **kwargs)


class HomeUpdatePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel
        fields = ['id', 'draft', 'product_status']

        # extra_kwargs = {"creator": {"read_only": True}}


class HomeAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel

        fields = ['isBookmarked', ]

        # extra_kwargs = {"creator": {"read_only": True}}


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


class HomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['title']


class HomeDetailSerializer(serializers.ModelSerializer):
    category = HomeCategorySerializer()
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


class ProductLinkSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = HouseModel
        fields = ('id', 'link')

    def get_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())


class HomeFilterNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel
        fields = ['number_of_rooms']


class HomeFilterObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel
        fields = ['object']
