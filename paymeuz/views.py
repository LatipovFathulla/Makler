from django.shortcuts import render
from rest_framework import generics
from payme.models import MerchantTransactionsModel
from paymeuz.serializers import TestMyMerchantSerializer

class MyTestListAPIView(generics.ListAPIView):
    queryset = MerchantTransactionsModel.objects.all()
    serializer_class = TestMyMerchantSerializer