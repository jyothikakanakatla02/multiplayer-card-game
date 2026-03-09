from django.urls import path

from .views import create_room_view,join_room,room_state
urlpatterns = [
    path("create-room/", create_room_view),
    path("join-room/", join_room, name="join-room"),
    path("room-state/<str:room_id>/", room_state),
]
