from rest_framework import permissions
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
            if response['status'] == "success":
                status = 201
            else:
                status = 400
            return Response(response, status=status)
        else:
            return Response(serializer.errors, status=400)


class UserLoginView(APIView):
    def post(self, request):
        response = authenticate_user(request)
        if response['status'] == "success":
            status = 201
        else:
            status = 400
        return Response(response, status=status)


class UserSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        response, status = search_user(request)
        return Response(response, status=status)


class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        response, status = create_friend_request(request)
        return Response(response, status=status)


class RespondFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        response, status = update_friend_request(pk, request)
        return Response(response, status=status)


class FriendListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friends = User.objects.filter(
            id__in=FriendRequest.objects.filter(
                from_user=request.user, status='accepted'
            ).values_list('to_user', flat=True)
        )
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
            build_response(status='success', data={'users': serializer.data})
        )
