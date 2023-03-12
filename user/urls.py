from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import UserProfile, UserList, UserDetailAPIView, UpdateProfileView, UserProductsList

# router = DefaultRouter()
# router.register('api/v1/signup', UserViewSet, 'signup')

urlpatterns = [
        # path('api/v1/users/', include('user.urls')),
        path('api/v1/profile/<int:pk>/', UserList.as_view()),
        path('api/v1/user-products/<int:pk>/', UserProductsList.as_view()),
        path('api/v1/get-user/<int:pk>/', UserDetailAPIView.as_view()),
        path('api/v1/update-user/<int:pk>/', UpdateProfileView.as_view()),
        path('api/v1/delete-user/<int:pk>/', UserDetailAPIView.as_view()),
        # path('profile/', UserProfile.as_view(), name='user-profile'),
]
