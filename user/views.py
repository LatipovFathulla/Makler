import random
from django.core.cache import cache

from django.contrib.auth import logout, authenticate
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from masters.models import MasterModel
from products.models import HouseModel
from store.models import StoreModel
from .models import CustomUser

from products.serializers import HomeSerializer
from masters.serializers import MasterSerializer
from store.serializers import StoreModelSerializer
from .playmobile import SUCCESS, SendSmsWithPlayMobile

from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer, UserALLSerializer, \
    UpdateUserSerializer, UserProductsSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        hashed_password = make_password(password)

        referrer_id = request.query_params.get('referrer')
        referrer = None
        if referrer_id:
            try:
                referrer = CustomUser.objects.get(id=referrer_id)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Invalid referrer ID'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = CustomUser.objects.get_or_create(phone_number=phone_number, defaults={'password': hashed_password})

        if created or not user.mycode:
            user.generate_mycode()

        if referrer:
            user.referrer = referrer
            user.save(update_fields=['referrer'])

            # Добавляем баллы пользователю X при успешной регистрации нового пользователя Y
            user.referrer.score += 1
            user.referrer.save(update_fields=['score'])

        sms_message = f"Ваш код подтверждения: {user.mycode}"
        playmobile_api = SendSmsWithPlayMobile(message=sms_message, phone=phone_number)
        sms_response = playmobile_api.send()

        if sms_response['status'] == SUCCESS:
            return Response({'token': user.tokens(), 'referrer_id': user.referrer_id})
        else:
            return Response({'error': 'Ошибка при отправке SMS-сообщения'})


class ConfirmationView(APIView):
    def post(self, request):
        mycode = request.data.get('confirmation_code')
        phone_number = request.data.get('phone_number')

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Пользователь с указанным номером телефона не найден.'},
                            status=status.HTTP_404_NOT_FOUND)

        if user.is_valid_mycode(mycode):
            refresh = RefreshToken.for_user(user)
            return Response({'message': 'Код подтверждения верный. Пользователь авторизован.',
                             'refresh': str(refresh),
                             'access': str(refresh.access_token),
                             'id': str(user.id)})
        else:
            return Response({'error': 'Код подтверждения неверный.'}, status=status.HTTP_400_BAD_REQUEST)


def generate_mycode(self):
    self.mycode = str(random.randint(1000, 9999))
    self.save(update_fields=['mycode'])
    return self.mycode


def save_mycode_in_cache(self):
    cache.delete(f"mycode_{self.phone_number}")
    cache.set(f"mycode_{self.phone_number}", self.mycode, version=str(self.mycode))


def is_valid_mycode(self, mycode):
    saved_mycode = cache.get(f"mycode_{self.phone_number}", version=mycode)
    return mycode == saved_mycode


def clear_mycode(self):
    self.mycode = None
    self.save(update_fields=['mycode'])
    cache.delete(f"mycode_{self.phone_number}")


class LoginView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ))
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        # Аутентификация пользователя
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'id': str(user.id)
            })
        else:
            return Response({'error': 'Неверные учетные данные.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserReferralsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        referrals = CustomUser.objects.filter(referrer=user)
        serializer = UserSerializer(referrals, many=True, context={'request': request})
        return Response(serializer.data)

#
# @action(['DELETE'], detail=False, permission_classes=[IsAuthenticated])
# def logout(self, request: Request):
#     Token.objects.get(user=request.user).delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


# class LoginView(TokenObtainPairView):
# permission_classes = (AllowAny,)
# serializer_class = MyTokenObtainPairSerializer
# from django.contrib.auth import login, authenticate
#
#
# class LoginView(APIView):
#     def post(self, request):
#         phone_number = request.data['phone_number']
#         password = request.data['password']
#         user = authenticate(phone=phone_number, password=password)
#         if not user:
#             login(request, user)

#
# class LoginView(GenericViewSet):
#     serializer_class = LoginSerializer
#     queryset = CustomUser.objects.all()
#
#     @action(['POST'], detail=False, permission_classes=[permissions.AllowAny])
#     def login(self, request: Request):
#         self.serializer_class = LoginSerializer
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         phone_number = serializer.validated_data['phone_number']
#         code = serializer.validated_data['code']
#         if int(code) == int(CustomUser.objects.get(phone_number=phone_number).mycode):
#
#             token, created = CustomUser.objects.get_or_create(phone_number=phone_number)
#             return Response({'token': token.tokens()})
#         else:
#             return Response(
#                 {'error': f"Code is not valid! {code}=!{CustomUser.objects.get(phone_number=phone_number).mycode}"})
#
#     @action(['POST'], detail=False, permission_classes=[permissions.IsAuthenticated])
#     def logout(self, request):
#         token = RefreshToken(request.data.get('refresh'))
#         token.blacklist()
#         if not token.blacklist():
#             return Response("Ошибка")
#         else:
#             return Response({"status": "Успешно"})


class UserProfile(APIView):
    get_serializer_class = None

    def get_object(self, user, pk=None):
        houses = HouseModel.objects.filter(creator=user)
        masters = MasterModel.objects.filter(owner=user)
        stores = StoreModel.objects.filter(creator=user)

        data = {
            'houses': houses,
            'masters': masters,
            'stores': stores,
        }
        return data

    def get(self, request, **kwargs):
        announcements = self.get_object(user=request.user)
        housesserializer = HomeSerializer(announcements.get('houses'), many=True).data
        mastersserializer = MasterSerializer(announcements.get('masters'), many=True).data
        storesserializer = StoreModelSerializer(announcements.get('stores'), many=True).data

        data = {
            'announcements': {'HOUSEMODEL': housesserializer, 'MASTERMODEL': mastersserializer,
                              'STORAGEMODEL': storesserializer}
        }
        return Response(data, status=200)


def premium_required(view_func):
    @login_required
    def _wrapped_view_func(request, *args, **kwargs):
        account = get_object_or_404(CustomUser, user=request.user)
        if not account.is_premium:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view_func


class UserList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        users = CustomUser.objects.get(id=pk)
        if users.is_premium:
            serializer = UserSerializer(users, context={'request': request})
            return Response(serializer.data)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)



class NewUserList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        users = CustomUser.objects.get(id=pk)
        serializer = UserSerializer(users, context={'request': request})
        return Response(serializer.data)


class UserProductsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        users = CustomUser.objects.get(id=pk)
        serializer = UserProductsSerializer(users, context={'request': request})
        return Response(serializer.data)


class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Получения данных пользователья(ЛК)",
        operation_description="Метод получения данных пользователья. Помимо типа данных и токен авторизации, передаётся только ID пользователья.",
    )
    def get(self, request, pk):
        users = CustomUser.objects.get(id=pk)
        serializer = UserALLSerializer(users, context={'request': request})
        return Response(serializer.data)


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UpdateUserSerializer


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        # Отозвать (инвалидировать) все активные токены пользователя
        tokens = Token.objects.filter(user=instance)
        for token in tokens:
            token.delete()

        # Удалить пользователя
        instance.delete()

        return Response({'message': 'Пользователь успешно удален'}, status=status.HTTP_204_NO_CONTENT)
