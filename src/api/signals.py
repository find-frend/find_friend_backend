from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender="users.FriendRequest")
def create_friendship(sender, instance, created, **kwargs):
    """Создает объект Friendship после принятия заявки на дружбу."""
    from users.models import Friendship
    if instance.status == "Accepted":
        Friendship.objects.get_or_create(
            initiator=instance.from_user, friend=instance.to_user
        )
