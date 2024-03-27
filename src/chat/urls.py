from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("start/", views.start_chat, name="start_chat"),
    path("<int:chat_id>/", views.get_chat, name="get_chat"),
    path("", views.chats, name="chats"),
]
