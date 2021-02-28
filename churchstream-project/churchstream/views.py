from django.views.generic import TemplateView, ListView
from campus.models import CampusModel

class HomePage(ListView):
    template_name = 'home.html'
    model = CampusModel

# class LogoutSuccess(TemplateView):
#     template_name = 'logout_success.html'
#     model = CampusModel

# def logout(*args, **kwargs):
#     resp = main_logout(*args, **kwargs)
#     resp['Refresh'] = '3;URL=/' # redirects after 3 seconds to /account/login
#     return resp
