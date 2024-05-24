from rest_framework.permissions import BasePermission


class  IsAdminOrStudentPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        print(request.user and request.user.is_authenticated and request.user.role in ['Admin', 'Manager'])
        return request.user and request.user.is_authenticated and request.user.role in ['Admin', 'Manager']