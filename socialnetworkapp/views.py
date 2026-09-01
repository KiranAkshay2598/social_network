from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from socialnetworkapp.models import FriendRequest
from socialnetworkapp.serializers import (
    UserInitSerializer,
    UserSerializer,
    FriendRequestSerializer
)
from socialnetworkapp.services import (
    create_user,
    authenticate_user,
    search_user,
    create_friend_request,
    update_friend_request,
    build_response
)


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserInitSerializer(data=request.data)

        if serializer.is_valid():
            response = create_user(serializer.validated_data)
            http_status = status.HTTP_201_CREATED if response.get('status') == "success" else status.HTTP_400_BAD_REQUEST
            return Response(response, status=http_status)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        response = authenticate_user(request)
        http_status = status.HTTP_200_OK if response.get('status') == "success" else status.HTTP_400_BAD_REQUEST
        return Response(response, status=http_status)


class UserSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        response, http_status = search_user(request)
        return Response(response, status=http_status)


class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response, http_status = create_friend_request(request)
        return Response(response, status=http_status)


class RespondFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        response, http_status = update_friend_request(pk, request)
        return Response(response, status=http_status)


class FriendListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sent_friends = FriendRequest.objects.filter(
            from_user=request.user, status='accepted'
        ).values_list('to_user_id', flat=True)
        
        received_friends = FriendRequest.objects.filter(
            to_user=request.user, status='accepted'
        ).values_list('from_user_id', flat=True)

        friend_ids = set(sent_friends).union(set(received_friends))
        friends = User.objects.filter(id__in=friend_ids)
        serializer = UserSerializer(friends, many=True)
        return Response(
            build_response(status='success', data={'users': serializer.data})
        )


class PendingFriendRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(
            to_user=request.user, status='pending'
        )
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(
            build_response(status='success', data={'requests': serializer.data})
        )
