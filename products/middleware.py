from django.utils.translation import activate


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if language:
            language = language.split(',')[0]
            activate(language)
            print(f"Activated language: {language}")  # Отладочный вывод
        response = self.get_response(request)
        return response
