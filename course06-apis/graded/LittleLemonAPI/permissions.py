from rest_framework.permissions import BasePermission

class Manager(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.groups.filter(name="manager").exists():
            return True
        return False
    
class DeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.groups.filter(name="delivery-crew").exists():
            return True
        return False
    
class Customer(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and not request.user.groups.all() and not request.user.is_superuser:
            return True
        return False