from rest_framework.throttling import UserRateThrottle

class SendFriendRequestThrottle(UserRateThrottle):
    scope = 'friend_request'
