from django.db import transaction
from django.shortcuts import get_object_or_404

from users.models import Friend


class FriendRequestService:

    @staticmethod
    def get_user_friend_requests(user):
        return Friend.objects.filter(initiator=user).select_related(
            'friend') | Friend.objects.filter(
            friend=user).select_related('initiator')

    @staticmethod
    def create_friend_request(serializer, user):
        serializer.save(initiator=user)

    @staticmethod
    @transaction.atomic
    def respond_to_friend_request(request_id, user, accept):
        friend_request = get_object_or_404(Friend, pk=request_id,
                                           initiator=user)
        if accept:
            friend_request.is_added = True
            friend_request.save()
            return "Заявка была принята."
        friend_request.delete()
        return "Заявка была отклонена."
