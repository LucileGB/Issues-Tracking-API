from rest_framework import permissions


class IsContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, project):
        if request.user.is_contributor(project) and request.method in permissions.SAFE_METHODS:
            return True

        else:
            return False

class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author_user_id.id == request.user.id:
            return True

        return False

class ContributorList(permissions.BasePermission):
    def has_permission(self, request, project):
        if request.method in permissions.SAFE_METHODS or request.method == 'DELETE' or request.method == 'POST':
            return True

        else:
            return False
