from django.urls import path
from .views import create_room_view,join_room,room_state,leave_room,start_game,select_identity_api,complete_identity_api,pass_card,get_player_hand_api,force_finish_round_api,reset_round_api,participate_in_star_api,set_rounds_api
urlpatterns = [
    path("create-room/", create_room_view),
    path("join-room/", join_room, name="join-room"),
    path("set-rounds/", set_rounds_api),
    path("room-state/<str:room_id>/", room_state),
    path("leave-room/", leave_room),
    path("start-game/", start_game),
    path("select-identity/", select_identity_api),
    path("complete-identity/", complete_identity_api),
    path("pass-card/", pass_card),
    path("my-cards/<str:room_id>/<str:player_id>/",get_player_hand_api),
    path("participate-in-star/", participate_in_star_api),
    path("force-finish-round/",force_finish_round_api),
    path("reset-round/",reset_round_api)
    
    
]

