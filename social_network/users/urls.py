from django.urls import path
from .views import SignupView, LoginView, UserSearchView, FriendRequestView, FriendListView, PendingRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/<int:pk>/', FriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('pending-requests/', PendingRequestsView.as_view(), name='pending-requests'),
]
