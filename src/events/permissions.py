from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsPremiumUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST','PUT','DELETE']:
            if request.user.is_authenticated and request.user.profile in ["PREMIUM","ADMIN"]:
                return True
            else:
                return False
        return True