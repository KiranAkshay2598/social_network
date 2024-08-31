from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Q
from socialnetworkapp.serializers import UserSerializer, FriendRequestSerializer
from socialnetworkapp.models import FriendRequest
from django.utils import timezone
from datetime import timedelta


def build_response(status, data):
    response = {
        'status': status,
        'data': data}
    return response


def create_user(data):
    try:
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        if User.objects.filter(username=email).exists():
            return_data = {
                "error": "User with this email already exists."
            }
            status = 'failure'
        else:
            user = User.objects.create_user(username=email, password=password, first_name=first_name, last_name=last_name)
            serializer = UserSerializer(user)
            return_data = {
                "user": serializer.data
            }
            status = 'success'
        response = build_response(status=status, data=return_data)
        return response
    except Exception as exc:
        return_data = {"error": str(exc)}
        response = build_response(status='failure', data=return_data)
        return response


def authenticate_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return_data = {
                "token": token.key,
                "user_id": user.id
            }
            status = 'success'
        else:
            return_data = {
                "error": "Invalid credentials.",
            }
            status = 'failure'
        response = build_response(status=status, data=return_data)
        return response
    except Exception as exc:
        return_data = {"error": str(exc)}
        response = build_response(status='failure', data=return_data)
        return response


def search_user(request):
    try:
        keyword = request.GET.get('search', '')
        if not keyword:
            return_data = {
                "error": "Search keyword is required.",
            }
            status = 'failure'
            status_code = 400
        else:
            if '@' in keyword:
                user = User.objects.filter(username__iexact=keyword).first()
                if user:
                    serializer = UserSerializer(user)
                    return_data = {
                        "user": serializer.data,
                    }
                    status = 'success'
                    status_code = 200
                else:
                    return_data = {
                        "error": "User not found",
                    }
                    status = 'failure'
                    status_code = 404
            else:
                users = User.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword))
                if not users:
                    return_data = {
                        "error": "No user's found",
                    }
                    status = 'failure'
                    status_code = 404
                else:
                    page = int(request.GET.get('page', 1))
                    per_page = 10
                    start = (page - 1) * per_page
                    end = start + per_page
                    paginated_users = users[start:end]
                    serializer = UserSerializer(paginated_users, many=True)
                    return_data = {
                        "user": serializer.data,
                    }
                    status = 'success'
                    status_code = 200
        response = build_response(status=status, data=return_data)
        return response, status_code
    except Exception as exc:
        return_data = {"error": str(exc)}
        response = build_response(status='failure', data=return_data)
        return response, 400


def create_friend_request(request):
    try:
        from_user = request.user
        to_user_id = request.data.get('to_user')
        if not to_user_id:
            return_data = {
                "error": "To user ID is required.",
            }
            status = 'failure'
            status_code = 400
        else:
            to_user = User.objects.filter(id=to_user_id).first()
            if not to_user:
                return_data = {
                    "error": "To User not foundd.",
                }
                status = 'failure'
                status_code = 404
            else:
                if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').exists():
                    return_data = {
                        "error": "Friend request already sent.",
                    }
                    status = 'failure'
                    status_code = 400
                elif FriendRequest.objects.filter(from_user=from_user, created_at__gte=timezone.now() - timedelta(minutes=1)).count() >= 3:
                    return_data = {
                        "error": "Too many requests. Try again later.",
                    }
                    status = 'failure'
                    status_code = 429
                else:
                    friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
                    serializer = FriendRequestSerializer(friend_request)
                    return_data = {
                        "friend_request": serializer.data,
                    }
                    status = 'success'
                    status_code = 201
        response = build_response(status=status, data=return_data)
        return response, status_code
    except Exception as exc:
        return_data = {"error": str(exc)}
        response = build_response(status='failure', data=return_data)
        return response, 400


def update_friend_request(friend_request_id, request):
    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id)
    except FriendRequest.DoesNotExist:
        return build_response(status='failure', data={"error": "Friend request not found."}), 404

    action = request.data.get('action')
    if action == 'accept':
        friend_request.status = 'accepted'
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return_data = {
            "friend_request": serializer.data,
        }
        status = 'success'
        status_code = 200
    elif action == 'reject':
        friend_request.status = 'rejected'
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return_data = {
            "friend_request": serializer.data,
        }
        status = 'success'
        status_code = 200
    else:
        return_data = {
            "error": "Invalid action.",
        }
        status = 'success'
        status_code = 400
    return build_response(status=status, data=return_data), status_code
