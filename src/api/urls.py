from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django_rest_passwordreset.urls import add_reset_password_urls_to_router
from rest_framework.routers import DefaultRouter

from .views import (
    EventViewSet,
    FriendRequestViewSet,
    InterestViewSet,
    MyUserViewSet,
)

app_name = "api"

router = DefaultRouter()


router.register("users", MyUserViewSet, basename="users")
router.register("events", EventViewSet, basename="events")
router.register("interests", InterestViewSet, basename="interests")
router.register(r"friends", FriendRequestViewSet, basename="friends")

add_reset_password_urls_to_router(router, base_path="users/reset_password")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
