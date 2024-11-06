from django.utils import timezone

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            request.user.is_online = True
            request.user.last_active = timezone.now()
            request.user.save()
            
        return response 