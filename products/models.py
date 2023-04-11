from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CategoryModel(models.Model):
    title = models.CharField(max_length=500, verbose_name=_('title'))
    subtitle = models.TextField(verbose_name=_('subtitle'), null=True)
    image = models.FileField(upload_to='category_image', verbose_name=_('image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class AmenitiesModel(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('title'))
    image = models.FileField(upload_to='amenities_images', verbose_name=_('image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Все удобства')
        verbose_name_plural = _('Все удобства')


class ImagesModel(models.Model):
    image = models.FileField(upload_to='house_test_image', null=True)

    def __str__(self):
        return f"127.0.0.1:7783{self.image.url}"


class PriceListModel(models.Model):
    price_t = models.CharField(max_length=10, verbose_name=_('price'), null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.price_t

    class Meta:
        verbose_name = _('Цена')
        verbose_name_plural = _('Цены')


class HowSaleModel(models.Model):
    title = models.CharField(max_length=300, null=True, verbose_name=_('Как продавать'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Как продавать')
        verbose_name_plural = _('Как продавать')


class HouseModel(models.Model):
    creator = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='houses', null=True,
                                blank=True, verbose_name=_('creator'))
    title = models.CharField(max_length=600, verbose_name=_('title'))
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, verbose_name=_('category'),
                                 related_name='category', null=True, blank=True
                                 )
    view_count = models.PositiveIntegerField(default=0, null=True, verbose_name=_('view count'), )
    descriptions = models.TextField(verbose_name=_('descriptions'))
    price = models.CharField(max_length=100, verbose_name=_('price'))
    # app_currency = models.CharField(max_length=10, verbose_name=_('app_currency'), null=True)
    # app_type = models.CharField(max_length=80, verbose_name=_('app_type'), null=True)
    # typeOfRent = models.CharField(max_length=90, verbose_name=_('typeOfRent'), null=True)
    # typeOfHouse = models.CharField(max_length=90, verbose_name=_('typeOfHouse'), null=True)
    # typeOfObject = models.CharField(max_length=90, null=True)
    app_ipoteka = models.BooleanField(default=False, null=True, verbose_name=_('app_ipoteka'))
    app_mebel = models.BooleanField(default=False, null=True, verbose_name=_('app_mebel'))
    app_new_building = models.BooleanField(default=False, null=True, verbose_name=_('app_new_building'))
    price_type = models.ForeignKey(PriceListModel, on_delete=models.CASCADE, related_name='price_types', null=True,
                                   verbose_name=_('price_type'))
    ADD_TYPE = (
        ('купить', 'Купить'),
        ('продать', 'Продать'),
        ('аденда', 'Аренда'),
    )
    type = models.CharField(
        max_length=200,
        choices=ADD_TYPE,
        default=ADD_TYPE[1],
        null=True,
        blank=True,
        verbose_name=_('type')
    )
    youtube_link = models.FileField(upload_to='Videos', verbose_name=_('youtube_link'), null=True, blank=True)
    web_address_title = models.CharField(max_length=400, verbose_name=_('web_address_title'), null=True)
    web_address_latitude = models.FloatField(verbose_name=_('web_address_latitude'), null=True)
    web_address_longtitude = models.FloatField(verbose_name=_('web_address_longtitude'), null=True)
    how_sale = models.ForeignKey(HowSaleModel, on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name=_('how_sale'))
    pm_general = models.CharField(max_length=400, verbose_name=_('pm_general'), null=True)
    # web_type = models.CharField(max_length=400, verbose_name=_('web_type'), null=True)
    # web_rental_type = models.CharField(max_length=400, verbose_name=_('web_rental_type'), null=True)
    pm_residential = models.CharField(max_length=500, verbose_name=_('pm_residential'), null=True)
    pm_kitchen = models.CharField(max_length=300, verbose_name=_('pm_kitchens'), null=True)
    # web_building_type = models.CharField(max_length=600, verbose_name=_('web_building_type'), null=True)
    RENTAL_TYPE = (
        ('длительно', 'Длительно'),
        ('несколько месяцев', 'несколько месяцев'),
        ('посуточно', 'посуточно')
    )
    rental_type = models.CharField(
        max_length=200,
        choices=RENTAL_TYPE,
        default=RENTAL_TYPE[1],
        null=True,
        blank=True,
        verbose_name=_("rental_type")
    )
    PROPERTY_TYPE = (
        ('жилая', 'жилая'),
        ('коммерческая', 'коммерческая')
    )
    OBJECT = (
        ('квартира', 'квартиру'),
        ('комната', 'комната'),
        ('дача', 'дача'),
        ('дома', 'дома'),
        ('участка', 'участка'),
        ('таунхаус', 'Townhouse'),
        ('спальное', 'Bed_space')
    )
    object = models.CharField(
        max_length=200,
        choices=OBJECT,
        default=None,
        null=True,
        blank=True,
        verbose_name=_('Object')
    )
    property_type = models.CharField(
        max_length=100,
        choices=PROPERTY_TYPE,
        default=PROPERTY_TYPE[1],
        null=True,
        verbose_name=_('property_type')
    )
    # images = models.ManyToManyField(ImagesModel, null=True, blank=True)
    # image = models.ImageField(upload_to='Product/APi', null=True)
    # general = models.CharField(max_length=90, verbose_name=_('general'))
    # residential = models.CharField(max_length=90, verbose_name=_('residential'))
    number_of_rooms = models.CharField(max_length=30, verbose_name=_('number_of_rooms'))
    floor = models.CharField(max_length=30, verbose_name=_('floor'))
    floor_from = models.CharField(max_length=30, verbose_name=_('floor_from'))
    BUILDING_TYPE = (
        ('кирпич', 'кирпич'),
        ('монолит', 'монолит'),
        ('панель', 'панель'),
        ('блочный', 'блочный')
    )
    building_type = models.CharField(
        max_length=50,
        choices=BUILDING_TYPE,
        default=None,
        verbose_name=_('building_type'),
        null=True,
        blank=True,
    )

    phone_number = models.CharField(max_length=19, verbose_name=_('phone_number'), null=True)
    amenities = models.ManyToManyField(AmenitiesModel, verbose_name=_('amenities'), related_name='pr_amenities',
                                       blank=True)
    isBookmarked = models.BooleanField(default=False, verbose_name=_('isBookmarked'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    draft = models.BooleanField(default=False, null=True, verbose_name=_('draft'))
    PRODUCT_STATUS = [
        (0, 'InProgress'),
        (1, 'PUBLISH'),
        (2, 'DELETED'),
        (3, 'ARCHIVED'),
        (4, 'REJECTED'),
    ]
    product_status = models.IntegerField(
        choices=PRODUCT_STATUS,
        default=0,
        null=True,
        verbose_name=_('product status'),
    )

    def __str__(self):
        return self.title

    @staticmethod
    def get_from_wishlist(request):
        wishlist = request.session.get('wishlist', [])
        return HouseModel.objects.filter(pk__in=wishlist)

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    # @property
    # def choices(self):
    #     return [{'rental_type': self.rental_type}, ['object', self.object], ['building_type', self.building_type]]

    class Meta:
        verbose_name = _('Маклер, (квартиры и т.д)')
        verbose_name_plural = _('Маклер, (квартиры и т.д)')
        ordering = ['-id']


class NewHouseImages(models.Model):
    product = models.ForeignKey(HouseModel, on_delete=models.CASCADE, related_name='images', verbose_name=_('product'))
    images = models.ImageField(upload_to='API/images', max_length=100, null=True, verbose_name=_('images'))


class HouseImageModel(models.Model):
    property_id = models.ForeignKey(HouseModel, null=False, default=1, on_delete=models.CASCADE,
                                    related_name='pr_images')
    image = models.ImageField(upload_to='house_images', verbose_name=_('image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    class Meta:
        verbose_name = _('Изображения маклер (квартиры и т.д)')
        verbose_name_plural = _('Изображения маклер (квартиры и т.д)')


class UserWishlistModel(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(HouseModel, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    class Meta:
        verbose_name = _('Избранное')
        verbose_name_plural = _('Избранные')

# class HouseOptionsModel(models.Model):
#     product = models.ForeignKey(HouseModel, on_delete=models.PROTECT, related_name='products_options',
#                                 verbose_name=_('product'), null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = _('product_options')
#         verbose_name_plural = _('product_options')
