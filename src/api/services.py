from django.db import transaction
from django.http import Http404

from events.models import EventMember, ParticipationRequest
from users.models import FriendRequest, Friendship


def handle_not_found(func):
    """Декоратор для обработки исключений ObjectDoesNotExist.

    Преобразует в Http404.
    """
    from functools import wraps

    from django.core.exceptions import ObjectDoesNotExist

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404("Заявка на дружбу не найдена.")

    return wrapper


class FriendRequestService:
    """Сервис для обработки бизнес-логики, связанной с заявками на дружбу."""

    @staticmethod
    @transaction.atomic
    @handle_not_found
    def accept_friend_request(request_id, user):
        """Принимает заявку на дружбу.

        Изменяет статус заявки на 'Принято' и создавая объект Friendship.
        """
        friend_request = FriendRequest.objects.get(
            pk=request_id, to_user=user, status="Pending"
        )
        friend_request.status = "Accepted"
        friend_request.save()
        Friendship.objects.get_or_create(
            initiator=friend_request.from_user, friend=friend_request.to_user
        )

    @staticmethod
    @transaction.atomic
    @handle_not_found
    def decline_friend_request(request_id, user):
        """Отклоняет заявку на дружбу, изменяя её статус на 'Отклонено'."""
        friend_request = FriendRequest.objects.get(
            pk=request_id, to_user=user, status="Pending"
        )
        friend_request.status = "Declined"
        friend_request.save()


class ParticipationRequestService:
    """Сервис для обработки заявок на участие в мероприятии."""

    @staticmethod
    @transaction.atomic
    @handle_not_found
    def accept_event_participation(request_id, user):
        """Принятие заявки на участие в мероприятии.

        Меняется статус заявки на "Принято", заполняется поле "Кем обработано".

        Cоздается объект EventMember.
        """
        participation_request = ParticipationRequest.objects.get(
            pk=request_id, status="Pending"
        )
        participation_request.status = "Accepted"
        participation_request.processed_by = user
        participation_request.save()
        EventMember.objects.get_or_create(
            user=participation_request.from_user,
            event=participation_request.event,
            is_organizer=False,
        )

    @staticmethod
    @transaction.atomic
    @handle_not_found
    def decline_event_participation(request_id, user):
        """Отклонение заявки на участие в мероприятии.

        Меняется статус заявки на "Отклонено".

        Заполняется поле "Кем обработано".
        """
        participation_request = ParticipationRequest.objects.get(
            pk=request_id, status="Pending"
        )
        participation_request.status = "Declined"
        participation_request.processed_by = user
        participation_request.save()
