import re
from django.contrib.auth.models import User
from rolepermissions.permissions import available_perm_status

def has_permission(self, request, view):

    name = self.__class__.__name__
    permission = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower().replace('is_','allow_')
    user = User.objects.get(username=request.user)
    perms = available_perm_status(user)
    
    if perms.get(permission):
        return True 
    return False 

def has_object_permission(self, request, view, obj):
    return True

def factory_get_permission(perm_class):
   _Class = type(perm_class, (object, ), {
       'has_permission': has_permission,
       'has_object_permission': has_object_permission
   })
   return _Class

perm = factory_get_permission

