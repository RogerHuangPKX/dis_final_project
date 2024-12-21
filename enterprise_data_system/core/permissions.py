from functools import wraps
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

def role_required(allowed_roles):
    """
    Decorator for views that checks whether a user has the required role.
    Usage:
        @role_required(['admin', 'analyst'])
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                raise PermissionDenied("Authentication required")
            
            # Superuser can access everything
            if request.user.is_superuser:
                return view_func(view_instance, request, *args, **kwargs)
            
            # Check user roles
            user_roles = get_user_roles(request.user)
            if not any(role in allowed_roles for role in user_roles):
                raise PermissionDenied(
                    f"Required roles: {', '.join(allowed_roles)}. "
                    f"User roles: {', '.join(user_roles)}"
                )
            
            return view_func(view_instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator

def get_user_roles(user):
    """
    Get list of roles for a user.
    For simplicity, we're using groups as roles.
    In a real system, you might want to use a more sophisticated role system.
    """
    roles = list(user.groups.values_list('name', flat=True))
    if user.is_staff:
        roles.append('admin')
    return roles

class RoleBasedPermission(permissions.BasePermission):
    """
    Permission class that checks user roles.
    Usage:
        class MyViewSet(viewsets.ModelViewSet):
            permission_classes = [RoleBasedPermission]
            required_roles = {
                'list': ['admin', 'analyst'],
                'create': ['admin'],
                'retrieve': ['admin', 'analyst', 'agent'],
                'update': ['admin'],
                'destroy': ['admin'],
            }
    """
    def has_permission(self, request, view):
        # Check if view has required roles defined
        if not hasattr(view, 'required_roles'):
            return True
        
        # Get required roles for the current action
        action = view.action or request.method.lower()
        required_roles = view.required_roles.get(action, [])
        
        # If no roles required, allow access
        if not required_roles:
            return True
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Superuser can access everything
        if request.user.is_superuser:
            return True
        
        # Check user roles
        user_roles = get_user_roles(request.user)
        return any(role in required_roles for role in user_roles)

class IsAdminUser(permissions.BasePermission):
    """
    Permission class that only allows admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class IsAnalystUser(permissions.BasePermission):
    """
    Permission class that allows admin and analyst users.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        user_roles = get_user_roles(request.user)
        return 'admin' in user_roles or 'analyst' in user_roles

class IsAgentUser(permissions.BasePermission):
    """
    Permission class that allows admin and agent users.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        user_roles = get_user_roles(request.user)
        return 'admin' in user_roles or 'agent' in user_roles
