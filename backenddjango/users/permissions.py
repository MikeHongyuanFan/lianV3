from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission to only allow admin users
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'


class IsAdminOrBroker(permissions.BasePermission):
    """
    Permission to only allow admin or broker users
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'broker']


class IsAdminOrBD(permissions.BasePermission):
    """
    Permission to only allow admin or BD users
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'bd']


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to only allow owners of an object or admin users
    """
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.role == 'admin':
            return True
        
        # Check if object has a user field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object has a created_by field
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return False
