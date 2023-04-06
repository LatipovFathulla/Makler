from django.urls import path
from rest_framework.routers import DefaultRouter
from products.views import HouseListAPIView, HouseDetailAPIView, HouseAddCreateAPIView, \
    APPHouseAddCreateAPIView, HouseUpdateAPIView, HouseDestroyAPIView, WebHomeCreateView, WebHomeListAPIView, \
    WebAmenitiesListAPIView, SearchWebHomeListAPIView, WishlistHouseDetailAPIView, UserWishlistModelView, \
    GetHouseFavListAPIView, RandomHouseModelAPIView, WishlistUserHouseDetailAPIView, PatchHouseUpdateAPIView, \
    ArchiveProductListView, AddWishlistHousePIView, HouseImageDestroyView

router = DefaultRouter()
# router.register(r'api/v1/houses/create', HouseAddCreateAPIView)
# router.register(r'api/v1/houses/app-create', APPHouseAddCreateAPIView)
router.register(r'api/v1/houses/wishlist-houses', UserWishlistModelView)
router.register(r'api/v1/houses/delete', HouseDestroyAPIView)
router.register(r'web/api/v1/web-houses/create', WebHomeCreateView)

urlpatterns = [
    # path('api/v1/app-houses/', HouseListAPIView.as_view()),
    # path('api/v1/houses/app-create', APPHouseAddCreateAPIView.as_view()),
    path('web/api/v1/all-web-houses/', WebHomeListAPIView.as_view()),
    path('api/v1/houses/updates/<int:pk>', HouseUpdateAPIView.as_view()),
    path('api/v1/houses/patch-updates/<int:pk>', PatchHouseUpdateAPIView.as_view()),
    path('api/v1/houses/add-wishlist/<int:pk>', AddWishlistHousePIView.as_view()),
    path('web/api/v1/all-web-houses/popular', RandomHouseModelAPIView.as_view()),
    path('web/api/v1/web-houses/search/', SearchWebHomeListAPIView.as_view()),
    path('api/v1/houses/get-wishlist-houses', GetHouseFavListAPIView.as_view()),
    path('api/v1/houses/archive/<int:pk>', ArchiveProductListView.as_view()),
    # path('api/v1/houses/delete-wishlist-houses/<int:pk>', UserWishlistDeleteView.as_view()),
    path('api/v1/houses/user-wishlist/<int:pk>', WishlistUserHouseDetailAPIView.as_view()),
    path('web/api/v1/houses/<int:pk>', HouseDetailAPIView.as_view(), name='product_detail'),
    path('api/v1/web-houses/amenities/', WebAmenitiesListAPIView.as_view()),
    path('houses/<int:product_id>/delete/<int:image_id>', HouseImageDestroyView.as_view(), name='image-delete'),
    # path('api/v1/houses/image/', HouseImageAPIView.as_view()),
]

urlpatterns += router.urls
