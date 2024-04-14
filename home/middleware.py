from django.http import HttpResponseRedirect
from django.urls import reverse


class RedirectAdminMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.resolver_match and request.resolver_match.url_name == 'admin':
            if not request.user.is_authenticated or not request.user.is_superuser:
                return HttpResponseRedirect(reverse('home'))
        
        return self.get_response(request)
    

