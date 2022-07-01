from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnerOrAdmins(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_admin
            or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class AuthorAndStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_admin or request.user.is_moderator
                    or (request.user.is_user
                        and request.user == obj.author)
                )
            )
        )


class AdminOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.is_admin
                    or request.user.is_staff is True
                    or request.user.is_superuser is True)
        return False

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin
                    or request.user.is_staff is True
                    or request.user.is_superuser is True)
        return False


class OnlyOwnAccount(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
