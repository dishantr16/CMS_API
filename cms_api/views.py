from rest_framework import generics, permissions, status
from .permissions import IsPostOwnerOrReadOnly, IsOwnerOrPublic
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Post, Like
from .serializers import UserSerializer, UserDetailSerializer, PostSerializer, PostDetailSerializer, LikeSerializer, LikeDetailSerializer


# Create your views here.


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

class CreatePostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(is_private=False) | queryset.filter(owner=self.request.user)
        else:
            queryset = queryset.filter(is_private=False)
        return queryset

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrPublic, IsPostOwnerOrReadOnly]
    queryset = Post.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('user').prefetch_related('likes')

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UpdatePostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            self.permission_denied(self.request)
        return obj

class DeletePostView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            self.permission_denied(self.request)
        return obj

class CreateLikeView(APIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        data = {'post': post_id, 'user': request.user.id}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LikeDetailView(generics.RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        if obj.post.is_private and obj.post.owner != self.request.user:
            self.permission_denied(self.request)
        return obj

class DeleteLikeView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            self.permission_denied(self.request)
        return obj
