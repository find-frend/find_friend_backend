from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from django_rest_passwordreset.urls import add_reset_password_urls_to_router

from .routers import CustomRouter
from .views import (CityViewSet, EventViewSet, FriendRequestViewSet,
                    InterestViewSet, MyUserViewSet, NotificationViewSet)

app_name = "api"

router = CustomRouter()

add_reset_password_urls_to_router(router, base_path="users/reset_password")

router.register("users", MyUserViewSet, basename="users")
router.register("events", EventViewSet, basename="events")
router.register("interests", InterestViewSet, basename="interests")
router.register("cities", CityViewSet, basename="cities")
router.register(r"friends", FriendRequestViewSet, basename="friends")
router.register(r"notification", NotificationViewSet, basename="notification")


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
    path("chats/", include("chat.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
