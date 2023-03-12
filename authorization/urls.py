from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.views import UserViewSet, LoginView

router = DefaultRouter()
router.register('', LoginView, 'auth')
router.register('signup', UserViewSet, 'register')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns += router.urls
