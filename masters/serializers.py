from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from products.models import MapModel
from user.models import CustomUser
from .models import MasterModel, MasterProfessionModel, MasterImagesModel, MasterUserWishlistModel, HowServiceModel


# master profiessions
class MasterProfessionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterProfessionModel
        fields = ['title']


# master address
class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapModel
        exclude = ['id', 'created_at']


# master images
class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterImagesModel
        fields = ['images']

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_url(obj.image.url)


class MasterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterImagesModel
        fields = ['images']

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_url(obj.image.url)


# all masters
class MasterSerializer(serializers.ModelSerializer):
    images = MasterImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    profession = MasterProfessionModelSerializer(many=True)

    # address = AddressModelSerializer()

    class Meta:
        model = MasterModel
        fields = ['pk', 'name', 'phone', 'address_title', 'address_latitude', 'address_longitude', 'avatar',
                  'profession', 'images', 'uploaded_images', 'email', 'password',
                  'experience', 'isBookmarked', 'draft', 'product_status', 'how_service', 'view_count', 'created_at',
                  'owner']


class UpdSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterModel
        fields = ['id', 'draft', 'owner', 'product_status']


class UpdMasterCreateSerializer(serializers.ModelSerializer):
    # profession = MasterProfessionModelSerializer(many=True)
    images = MasterImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )
    password = serializers.CharField(write_only=True, required=False, )

    # address = AddressModelSerializer()

    class Meta:
        model = MasterModel
        fields = ['name', 'email', 'phone', 'avatar', 'address_title', 'address_latitude', 'address_longitude',
                  'password', 'profession', 'how_service', 'images', 'uploaded_images',
                  'descriptions', 'experience', 'owner',
                  ]
        extra_kwargs = {"owner": {"read_only": True}}

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', None)
        # получаем новые изображения из запроса
        if uploaded_images:
            # если были загружены новые изображения, то сохраняем их
            instance.images.all().delete()
            for image in uploaded_images:
                MasterImagesModel.objects.create(master=instance, images=image)
        else:

            images_data = validated_data.pop('images', None)
            if images_data:
                instance.images.all().update(**images_data[0])
        return super().update(instance, validated_data)

# create master POST
class MasterCreateSerializer(serializers.ModelSerializer):
    # profession = MasterProfessionModelSerializer(many=True)
    images = MasterImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    password = serializers.CharField(write_only=True, required=False, )

    # address = AddressModelSerializer()

    class Meta:
        model = MasterModel
        fields = ['name', 'email', 'phone', 'avatar', 'address_title', 'address_latitude', 'address_longitude',
                  'password', 'profession', 'how_service', 'images', 'uploaded_images',
                  'descriptions', 'experience', 'owner',
                  ]
        extra_kwargs = {"owner": {"read_only": True}}

    def create(self, validated_data):
        profession = validated_data.get('profession')
        mw_uploaded_images = validated_data.pop('uploaded_images')
        owner = self.context['request'].user
        print(owner, 'this is owner')
        mastermodel = MasterModel.objects.create(
            name=validated_data['name'],
            owner=owner,
            password=validated_data['password'],
            how_service=validated_data['how_service'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            avatar=validated_data['avatar'],
            address_title=validated_data['address_title'],
            address_latitude=validated_data['address_latitude'],
            address_longitude=validated_data['address_longitude'],
            descriptions=validated_data['descriptions'],
            experience=validated_data['experience'],
        )
        for i in validated_data['profession']:
            mastermodel.profession.add(i.id)
            mastermodel.save()
        for mw_img in mw_uploaded_images:
            mw_up = MasterImagesModel.objects.create(master=mastermodel, images=mw_img)
        return mastermodel

    def get_img_url(self, obj):
        urls = []
        for i in obj.images.all():
            myurl = self.context['request'].build_absolute_uri(i.image.url)
            urls.append(myurl)
        return urls


class MasterDetailSerializer(serializers.ModelSerializer):
    images = MasterImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    profession = MasterProfessionModelSerializer(many=True)

    class Meta:
        model = MasterModel
        exclude = ['password']

    def get_img_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'posts']


class MasterUserWishlistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterUserWishlistModel
        fields = '__all__'


class MasterGetUserWishlistModelSerializer(serializers.ModelSerializer):
    user = CustomUser()
    master = MasterSerializer()

    class Meta:
        model = MasterUserWishlistModel
        fields = '__all__'


class MasterProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterProfessionModel
        fields = ['id', 'title']


# APP Master create
class APPMasterCreateSerializer(serializers.ModelSerializer):
    images = MasterImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    password = serializers.CharField(write_only=True, required=False, )

    # address = AddressModelSerializer()

    class Meta:
        model = MasterModel
        fields = ['name', 'email', 'phone', 'avatar', 'address_title', 'address_latitude', 'address_longitude',
                  'password', 'profession', 'how_service', 'images', 'uploaded_images',
                  'descriptions', 'experience', 'owner',
                  ]
        extra_kwargs = {"owner": {"read_only": True}}

    def create(self, validated_data):
        owner = self.context['request'].user
        m_uploaded_images = validated_data.pop('uploaded_images')
        mastermodel = MasterModel.objects.create(
            name=validated_data['name'],
            owner=owner,
            password=validated_data['password'],
            how_service=validated_data['how_service'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            avatar=validated_data['avatar'],
            address_title=validated_data['address_title'],
            address_latitude=validated_data['address_latitude'],
            address_longitude=validated_data['address_longitude'],
            descriptions=validated_data['descriptions'],
            experience=validated_data['experience'],
        )
        for i in validated_data['profession']:
            mastermodel.profession.add(i.id)
            mastermodel.save()
        for m_img in m_uploaded_images:
            mr_uploaded_images = MasterImagesModel.objects.create(master=mastermodel, images=m_img)
        return mastermodel

    def get_img_url(self, obj):
        urls = []
        for i in obj.images.all():
            myurl = self.context['request'].build_absolute_uri(i.image.url)
            urls.append(myurl)
        return urls

    def to_representation(self, instance):
        context = super().to_representation(instance)
        # context['profession'] = MasterProfessionModelSerializer(instance.profession, many=True).data
        # context['images'] = ImageModelSerializer(instance.images, many=True).data
        return context


class HowServiceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowServiceModel
        fields = ['id', 'title']
