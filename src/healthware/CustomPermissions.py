from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser and request.user.is_staff) or request.user.user_type == 'P';

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser and request.user.is_staff) or request.user.user_type == 'D';

class IsAuthDoctor(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser and request.user.is_staff) or request.user.user_type == 'D';
class IsActive(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active;
