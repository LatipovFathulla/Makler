from rest_framework import serializers

from mebel.models import MebelCategoryModel, MebelModel, NewMebelImages
from products.serializers import PriceListSerializer


class MebelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MebelCategoryModel
        fields = '__all__'


class MebelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewMebelImages
        fields = ['images']

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_url(obj.image.url)


class AllMebelSerializer(serializers.ModelSerializer):
    images = MebelImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    category = MebelCategorySerializer()
    price_type = PriceListSerializer()

    class Meta:
        model = MebelModel
        fields = '__all__'
        extra_kwargs = {"creator": {"read_only": True}}


class UpdateAllMebelSerializer(serializers.ModelSerializer):
    # images = MebelImageSerializer(many=True, read_only=True)
    # uploaded_images = serializers.ListField(
    #     child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
    #     write_only=True
    # )

    class Meta:
        model = MebelModel
        fields = '__all__'
        extra_kwargs = {"creator": {"read_only": True},}


class PatchUpdateAllMebelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MebelModel
        fields = ['id', 'draft', 'creator', 'product_status']


class MebelSerializer(serializers.ModelSerializer):
    images = MebelImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = MebelModel
        fields = '__all__'
        extra_kwargs = {"creator": {"read_only": True}}

    def create(self, validated_data):
        creator = self.context['request'].user
        mbl_uploaded_images = validated_data.pop('uploaded_images')
        mebelmodel = MebelModel.objects.create(
            title=validated_data['title'],
            category=validated_data['category'],
            price=validated_data['price'],
            price_type=validated_data['price_type'],
            short_descriptions=validated_data['short_descriptions'],
            long_descriptions=validated_data['long_descriptions'],
            phone_number=validated_data['phone_number'],
            web_address_title=validated_data['web_address_title'],
            web_address_latitude=validated_data['web_address_latitude'],
            web_address_longtitude=validated_data['web_address_longtitude'],
            creator=creator,
        )
        for mbl_img in mbl_uploaded_images:
            mb_uploaded_images = NewMebelImages.objects.create(product=mebelmodel, images=mbl_img)
        return mebelmodel
