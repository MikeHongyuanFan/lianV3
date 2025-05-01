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


class IsAdminOrBrokerOrBD(permissions.BasePermission):
    """
    Permission to only allow admin, broker, or BD users
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'broker', 'bd']


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


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permission to only allow users to access their own details or admin users to access any user details
    """
    def has_permission(self, request, view):
        # Admin can do anything
        if request.user and request.user.role == 'admin':
            return True
            
        # For retrieve action, check if the user is requesting their own details
        if view.action == 'retrieve':
            return True
            
        # For other actions, deny access to non-admin users
        return False
        
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.role == 'admin':
            return True
            
        # Users can only access their own details
        return obj.id == request.user.id