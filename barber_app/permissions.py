# barber_app/permissions.py
from rest_framework.permissions import BasePermission

class IsSuperAdminOrDev(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['super_admin', 'dev']
