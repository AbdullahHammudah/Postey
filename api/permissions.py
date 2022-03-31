from rest_framework.permissions import BasePermission

class PostsPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.type == 'moderate':
            return True