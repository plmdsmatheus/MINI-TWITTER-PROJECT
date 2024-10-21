from django.urls import path 
from .views import FollowUserView, FollowersListView, FollowingListView

urlpatterns = [
    path("follow/<str:username>/", FollowUserView.as_view(), name="follow-user"),
    path("followers/<str:username>/", FollowersListView.as_view(), name="followers-list"),
    path("following/<str:username>/", FollowingListView.as_view(), name="following-list"),
]