from django.urls import path
from .views import create_room_view,join_room,room_state,leave_room,start_game,select_identity_api,complete_identity_api
urlpatterns = [
    path("create-room/", create_room_view),
    path("join-room/", join_room, name="join-room"),
    path("room-state/<str:room_id>/", room_state),
    path("leave-room/", leave_room),
    path("start-game/", start_game),
    path("select-identity/", select_identity_api),
    path("complete-identity/", complete_identity_api)
]

