from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows full access to admins, read-only access to everyone else.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and getattr(request.user, 'user_type', None) == 'admin'


class IsBuyer(permissions.BasePermission):
    """
    Allows access only to buyers.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'user_type', None) == 'buyer'


class IsSeller(permissions.BasePermission):
    """
    Allows access only to sellers.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'user_type', None) == 'seller'


class IsBuyerOrSeller(permissions.BasePermission):
    """
    Allows access to buyers or sellers, and checks object ownership.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            getattr(request.user, 'user_type', None) in ['buyer', 'seller']
        )

    def has_object_permission(self, request, view, obj):
        if getattr(request.user, 'user_type', None) == 'buyer':
            return getattr(obj, 'buyer', None) == request.user
        elif getattr(request.user, 'user_type', None) == 'seller':
            return getattr(obj, 'seller', None) == request.user
        return False
    
class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access to everyone, but write access only to sellers.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.user_type == 'seller'