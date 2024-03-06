from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CityViewSet,
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
router.register("cities", CityViewSet, basename="cities")
router.register(r"friends", FriendRequestViewSet, basename="friends")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
