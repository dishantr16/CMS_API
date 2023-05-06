from rest_framework import permissions


class IsPostOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsOwnerOrPublic(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # if obj.is_public:
        #     return True
        if obj.visibility == 'public':
            return True

        return obj.user == request.user
