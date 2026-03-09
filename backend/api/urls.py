from django.urls import path

from .views import create_room_view,join_room,leave_room
urlpatterns = [
    path("create-room/", create_room_view),
    path("join-room/", join_room, name="join-room"),
    path("leave-room/", leave_room)
]
