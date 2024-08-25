from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import FriendRequest, CustomUser
from .serializers import UserSerializer, FriendRequestSerializer


class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = CustomUser.objects.filter(email__iexact=email).first()
        if user and user.check_password(password):
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginate_by = 10

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return CustomUser.objects.filter(Q(email__iexact=query) | Q(username__icontains=query))


class FriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        to_user_email = request.data.get('email')
        to_user = CustomUser.objects.filter(email=to_user_email).first()
        if not to_user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status='pending').exists():
            return Response({"message": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        friend_request = FriendRequest.objects.filter(id=pk, to_user=request.user).first()
        if not friend_request:
            return Response({"message": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action == 'accept':
            friend_request.status = 'accepted'
        elif action == 'reject':
            friend_request.status = 'rejected'
        else:
            return Response({"message": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.save()
        return Response({"message": f"Friend request {action}ed"}, status=status.HTTP_200_OK)


class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(Q(from_user=user) | Q(to_user=user), status='accepted')
        friend_ids = [fr.to_user.id if fr.from_user == user else fr.from_user.id for fr in friends]
        return CustomUser.objects.filter(id__in=friend_ids)


class PendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')
