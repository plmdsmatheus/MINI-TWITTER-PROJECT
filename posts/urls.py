from django.urls import path
from .views import PostListCreateView, PostDetailView, LikePostView, UserFeedView

urlpatterns = [
    path("", PostListCreateView.as_view(), name="post-list-create"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/like/", LikePostView.as_view(), name="like-post"),
    path("feed/", UserFeedView.as_view(), name="user-feed"),
]