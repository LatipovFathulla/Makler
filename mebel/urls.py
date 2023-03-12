from django.urls import path
# MebelCategoryListAPIView
# MebelListAPIView
from rest_framework.routers import DefaultRouter

from mebel.views import MebelCategoryListAPIView, MebelListAPIView, MebelCreateAPIView, MebelUpdateView, \
    MebelDestroyAPIView, MebelDetailAPIView, RandomMebelListAPIView, PatchMebelUpdateView

router = DefaultRouter()
router.register(r'api/v1/mebels/create', MebelCreateAPIView)
router.register(r'api/v1/mebels/delete', MebelDestroyAPIView)

urlpatterns = [
    path('api/v1/mebel-categories/', MebelCategoryListAPIView.as_view()),
    path('api/v1/mebels/', MebelListAPIView.as_view()),
    path('api/v1/mebels/popular', RandomMebelListAPIView.as_view()),
    path('api/v1/mebels/<int:pk>', MebelDetailAPIView.as_view()),
    path('api/v1/mebels/update/<int:pk>', MebelUpdateView.as_view()),
    path('api/v1/mebels/patch-update/<int:pk>', PatchMebelUpdateView.as_view()),
]

urlpatterns += router.urls
