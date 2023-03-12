from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from user.models import CustomUser
from .models import StoreModel, StoreAmenities, UseForModel, HowStoreServiceModel, StoreBrandModel


# bu store niki
class StoreAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAmenities
        fields = ['id', 'title']


class UseForModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseForModel
        fields = ['id', 'title']


class HowStoreServiceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowStoreServiceModel
        fields = ['id', 'title']


class UpdateStoreModelSerializer(serializers.ModelSerializer):
    use_for = UseForModelSerializer

    class Meta:
        model = StoreModel
        fields = ['id', 'name', 'description', 'store_amenitites', 'brand_title', 'price',
                  'price_type', 'use_for', 'how_store_service',
                  'phoneNumber', 'address', 'email', 'created_at', 'isBookmarked', 'draft', 'product_status', 'creator']
        extra_kwargs = {"creator": {"read_only": True}}


class PatchStoreUpdateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreModel
        fields = ['id', 'draft', 'creator', 'product_status']


class StoreBrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreBrandModel
        fields = ['id', 'title']


class ALLStoreModelSerializer(serializers.ModelSerializer):
    store_amenitites = StoreAmenitiesSerializer(many=True)
    use_for = UseForModelSerializer()
    brand_title = StoreBrandModelSerializer()

    class Meta:
        model = StoreModel
        fields = ['id', 'name', 'image', 'brand_image', 'description', 'store_amenitites', 'brand_title', 'price',
                  'price_type', 'use_for', 'how_store_service',
                  'phoneNumber', 'address', 'email', 'created_at', 'isBookmarked', 'draft', 'product_status',
                  'view_count', 'creator']


class ProfileStoreModelSerializer(serializers.ModelSerializer):
    # creator = serializers.CharField(source='creator')
    # uploaded_image = serializers.FileField(
    #     max_length=10000,
    #     allow_empty_file=False,
    #     write_only=True
    # )
    store_amenitites = StoreAmenitiesSerializer(many=True)
    use_for = UseForModelSerializer

    class Meta:
        model = StoreModel
        fields = ['id', 'name', 'image', 'brand_image', 'description', 'store_amenitites', 'brand_title', 'price',
                  'price_type', 'use_for', 'how_store_service',
                  'phoneNumber', 'address', 'email', 'created_at', 'isBookmarked', 'draft', 'product_status',
                  'view_count', 'creator']
        extra_kwargs = {"creator": {"read_only": True}}


class StoreModelSerializer(serializers.ModelSerializer):
    # creator = serializers.CharField(source='creator')
    # uploaded_image = serializers.FileField(
    #     max_length=10000,
    #     allow_empty_file=False,
    #     write_only=True
    # )
    use_for = UseForModelSerializer

    class Meta:
        model = StoreModel
        fields = ['id', 'name', 'image', 'brand_image', 'description', 'store_amenitites', 'brand_title', 'price',
                  'price_type', 'use_for', 'how_store_service',
                  'phoneNumber', 'address', 'email', 'created_at', 'isBookmarked', 'draft', 'product_status',
                  'view_count', 'creator']
        extra_kwargs = {"creator": {"read_only": True}}
        # read_only_fields = ['creator', ]

    def create(self, validated_data):
        creator = self.context['request'].user
        storemodel = StoreModel.objects.create(creator=creator,
                                               name=validated_data['name'],
                                               description=validated_data['description'],
                                               image=validated_data['image'],
                                               brand_image=validated_data['brand_image'],
                                               brand_title=validated_data['brand_title'],
                                               price=validated_data['price'],
                                               how_store_service=validated_data['how_store_service'],
                                               price_type=validated_data['price_type'],
                                               use_for=validated_data['use_for'],
                                               phoneNumber=validated_data['phoneNumber'],
                                               address=validated_data['address'],
                                               email=validated_data['email'],
                                               )
        for u in validated_data['store_amenitites']:
            storemodel.store_amenitites.add(u.id)
            storemodel.save()
        return storemodel

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)
