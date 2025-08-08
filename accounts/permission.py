from rest_framework.permissions import BasePermission



class IsLandlordUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'landlord_user')



class IsTenantUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'tenant_user')



class IsOwnerLandlordOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if hasattr(obj, 'owner'):
            return obj.owner == getattr(request.user, 'landlord_user', None)

        if hasattr(obj, 'apartment'):
            return obj.apartment.owner == getattr(request.user, 'landlord_user', None)

        return False



class IsOwnerTenantOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.owner == request.user.tenant_user
