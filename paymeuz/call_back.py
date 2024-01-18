from payme.views import MerchantAPIView


class PaymeCallBackAPIView(MerchantAPIView):
    def create_transaction(self, user_id, action, *args, **kwargs) -> None:
        print(f"create_transaction for user_id: {user_id}, response: {action}")

    def perform_transaction(self, user_id, action, *args, **kwargs) -> None:
        print(f"perform_transaction for user_id: {user_id}, response: {action}")

    def cancel_transaction(self, user_id, action, *args, **kwargs) -> None:
        print(f"cancel_transaction for user_id: {user_id}, response: {action}")
