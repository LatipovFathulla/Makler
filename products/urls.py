from django.urls import path
from rest_framework.routers import DefaultRouter
from products.views import HouseListAPIView, HouseDetailAPIView, HouseAddCreateAPIView, \
    HouseUpdateAPIView, HouseDestroyAPIView, WebHomeCreateView, WebHomeListAPIView, \
    WebAmenitiesListAPIView, SearchWebHomeListAPIView, WishlistHouseDetailAPIView, UserWishlistModelView, \
    GetHouseFavListAPIView, RandomHouseModelAPIView, WishlistUserHouseDetailAPIView, PatchHouseUpdateAPIView, \
    ArchiveProductListView, AddWishlistHousePIView, HouseImageDestroyView, HomeFilterNumberView, HomeFilterObjectView, \
    ComplaintReasonsListView, ComplaintCreateView

router = DefaultRouter()
router.register(r'api/v1/houses/wishlist-houses', UserWishlistModelView)
router.register(r'api/v1/houses/delete', HouseDestroyAPIView)
router.register(r'web/api/v1/web-houses/create', WebHomeCreateView)

urlpatterns = [
    path('web/api/v1/all-web-houses/', WebHomeListAPIView.as_view()),
    path('api/v1/houses/updates/<int:pk>', HouseUpdateAPIView.as_view()),
    path('api/v1/houses/patch-updates/<int:pk>', PatchHouseUpdateAPIView.as_view()),
    path('api/v1/houses/add-wishlist/<int:pk>', AddWishlistHousePIView.as_view()),
    path('web/api/v1/all-web-houses/popular', RandomHouseModelAPIView.as_view()),
    path('web/api/v1/web-houses/search/', SearchWebHomeListAPIView.as_view()),
    path('api/v1/houses/get-wishlist-houses', GetHouseFavListAPIView.as_view()),
    path('api/v1/houses/archive/<int:pk>', ArchiveProductListView.as_view()),
    path('api/v1/houses/user-wishlist/<int:pk>', WishlistUserHouseDetailAPIView.as_view()),
    path('web/api/v1/houses/<int:pk>', HouseDetailAPIView.as_view(), name='product_detail'),
    path('api/v1/web-houses/amenities/', WebAmenitiesListAPIView.as_view()),
    path('houses/<int:product_id>/delete/<int:image_id>', HouseImageDestroyView.as_view(), name='image-delete'),
    path('houses/filter-web/rooms', HomeFilterNumberView.as_view(), name='filter-rooms'),
    path('houses/filter-web/objects', HomeFilterObjectView.as_view(), name='filter-rooms'),
    path('houses/complaints/', ComplaintReasonsListView.as_view(), name='complaint'),
    path('houses/complaints/create', ComplaintCreateView.as_view(), name='complaint-create'),
]

urlpatterns += router.urls
