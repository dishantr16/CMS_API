from django.urls import path
from .views import CreateUserView, UserDetailView, CreatePostView, PostListView, PostDetailAPIView, UpdatePostView, DeletePostView, CreateLikeView, LikeDetailView, DeleteLikeView

 
urlpatterns = [
    path('users/', CreateUserView.as_view(), name='create_user'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('posts/', CreatePostView.as_view(), name='create_post'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/<int:pk>/update/', UpdatePostView.as_view(), name='update_post'),
    path('posts/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('likes/<int:post_id>/', CreateLikeView.as_view(), name='create_like'),
    path('likes/<int:pk>/', LikeDetailView.as_view(), name='like_detail'),
    path('likes/<int:pk>/delete/', DeleteLikeView.as_view(), name='delete_like'),
    path('posts/all/', PostListView.as_view(), name='post_list'),
]
