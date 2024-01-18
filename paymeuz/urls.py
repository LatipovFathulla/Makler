from django.urls import path

from paymeuz.pay_link import GeneratePayLinkAPIView

urlpatterns = [
    path('pay-link/', GeneratePayLinkAPIView.as_view(), name='generate-pay-link')
]
