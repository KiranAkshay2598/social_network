from django.urls import path
from socialnetworkapp import views

urlpatterns = [
    path('api/v1/signup/', views.UserSignupView.as_view(), name='user-signup'),
    path('api/v1/login/', views.UserLoginView.as_view(), name='user-login'),
    path('api/v1/search/', views.UserSearchView.as_view(), name='user-search'),
    path('api/v1/send-request/', views.SendFriendRequestView.as_view(), name='send-friend-request'),
    path('api/v1/respond-request/<int:pk>/', views.RespondFriendRequestView.as_view(), name='respond-friend-request'),
    path('api/v1/friends/', views.FriendListView.as_view(), name='friend-list'),
    path('api/v1/pending-requests/', views.PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]
