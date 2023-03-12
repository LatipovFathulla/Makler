"""makler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from carousel.views import CarouselModelAPIView
from .yasg import urlpatterns as doc_urls
from rest_framework.routers import DefaultRouter

from products.views import CategoryListAPIView, AmenitiesListAPIView, HouseFavListAPIView, WebAmenitiesListAPIView, \
    WebPriceListAPIView, snippet_list

from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
# router.register(r'api/v1/maklers/create', MasterAddCreateAPIView)


urlpatterns = [
    path('master/', include('masters.urls'), name='masters'),
    path('store2/', include('store.urls'), name='store'),
    path('users/', include('user.urls')),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls'), name='products'),
    path('mebel/', include('mebel.urls'), name='mebel'),
    path('authorization/', include('authorization.urls')),
    path('api/v1/categories/', CategoryListAPIView.as_view()),
    path('api/v1/amenities/', AmenitiesListAPIView.as_view()),
    path('api/v1/carousels/', CarouselModelAPIView.as_view()),
    path('web/api/v1/web-amenities/', WebAmenitiesListAPIView.as_view()),
    path('web/api/v1/web-prices/', WebPriceListAPIView.as_view()),
    path('api/v1/fav/', HouseFavListAPIView.as_view()),

    # path('posts/', PostList.as_view()),
    # path('posts/<int:pk>/', PostDetail.as_view()),
    # path('web/api/v1/web-houses/', WebHomeCreateView.as_view()),
    # path('api/v1/houses/create/', HouseAddCreateAPIView.as_view()),
    # path('api/v1/houses/archived/', HouseArchiveListAPIView.as_view()),
    # path('api/v1/login', LoginView.as_view()),
    # path('api/v1/auth/', include('djoser.urls.authtoken')),
    # path('api/v1/store/create/', StoreAddCreateAPIView.as_view()),
    # path('web/api/v1/web-houses', WebHomeCreateView),
    # path('user/', include()),
    # path('web2/', snippet_list),
]

urlpatterns += doc_urls
urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
