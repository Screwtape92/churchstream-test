from django import template
from campus.models import CampusModel

register = template.Library()

@register.filter
def campusid(value): # Only one argument.
    campusobj = CampusModel.objects.get(user=value)
    return campusobj.campus_name
