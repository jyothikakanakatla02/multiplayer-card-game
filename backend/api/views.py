from players.player import Player
<<<<<<< HEAD
from rooms.storage import create_room,pass_card_logic,get_player_hand_logic,force_finish_round_logic,reset_round_logic,participate_in_star_logic,set_total_rounds_logic
from rooms.constants import ROUND_RESULT
=======
from rooms.storage import create_room,pass_card_logic,get_player_hand_logic,force_finish_round_logic,reset_round_logic,participate_in_star_logic
from rooms.constants import ROUND_RESULT,IN_GAME,GAME_OVER
>>>>>>> origin/feature/set-round
from rest_framework.response import Response
from rest_framework.decorators import api_view
@api_view(["POST"])
def create_room_view(request):
    nickname = request.data["nickname"]
    avatar = request.data["avatar"]
    player = Player(nickname,avatar)
    room_id = create_room(player)
    return Response({
        "room_id" : room_id,
        "player_id" : player.player_id,
        "nickname" : player.nickname,
        "avatar" : player.avatar
    })
from rest_framework import status
from players.player import Player
from rooms.storage import add_player_to_room, remove_player_from_room, start_game_logic,select_identity_logic,complete_identity_phase_logic
@api_view(["POST"])
def join_room(request):
    room_id = request.data.get("room_id")
    nickname = request.data.get("nickname")
    avatar = request.data.get("avatar")
    if room_id is None or nickname is None or avatar is None:
        return Response(
            {"status" : "error",
             "message" : "Required fields are missing"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    room_id = room_id.strip()
    if not room_id:
        return Response(
            {"status" : "error",
             "message" : "Room ID cannot be empty"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try:
        player = Player(nickname, avatar)
    except ValueError as e:
        return Response(
            {"status" : "error",
             "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try:
        add_player_to_room(room_id, player)
    except Exception as e:
        return Response(
            {"status" : "error",
             "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
            )
    return Response(
        {"status" : "success",
         "room_id" : room_id,
         "player_id" : player.player_id
        }
        )
from rooms.storage import get_room
@api_view(["GET"])
def room_state(request,room_id):
    try:
        room = get_room(room_id)
    except ValueError as e:
        return Response(
            {
                "status" : "error",
                "message" : str(e)
            },
            status = status.HTTP_404_NOT_FOUND
        )
    if hasattr(room, "deck"):
        deck_remaining = len(room.deck)
    else:
        deck_remaining = None
    if hasattr(room, "current_turn_player_id"):
        current_turn_id = room.current_turn_player_id
    else:
        current_turn_id = None
    players_data = []
    current_turn_nickname = None
    winner_id = getattr(room, "round_winner", None)
    star_player_id = getattr(room,"star_player_id", None)
    star_player_nickname = None
    round_winner_nickname = None
    for player in room.players:
        if player.player_id == room.host_player_id:
            is_host = True
        else:
            is_host = False
        if player.player_id == current_turn_id:
            current_turn_nickname = player.nickname
        if player.player_id == winner_id :
            round_winner_nickname = player.nickname
        if player.player_id == star_player_id :
            star_player_nickname = player.nickname
        players_data.append({"nickname":player.nickname,
                             "avatar": player.avatar,
                             "cards_count": len(player.cards),
                             "score":player.score,
                             "is_host" : is_host})
    return Response({
        "status" : "success",
        "room_id" : room_id,
        "state" : room.state,
        "total_players" : len(players_data),
        "round_winner_player_id" : winner_id,
        "round_winner_nickname" : round_winner_nickname,
        "current_turn_player_id" : current_turn_id if room.state == IN_GAME else None,
        "current_turn_nickname" : current_turn_nickname,
        "deck_remaining" : deck_remaining f room.state == IN_GAME else 0,
        "players" : players_data,
        "scores_snapshot" : room.scores_snapshot,
        "star_player_nickname" : star_player_nickname if room.state == GAME_OVER else None,
        "round_scores": room.round_scores if room.state in [ROUND_RESULT, GAME_OVER] else None
    })
@api_view(["POST"])
def leave_room(request):
    room_id = request.data.get("room_id")
    player_id = request.data.get("player_id")
    if room_id is None or player_id is None:
        return Response(
            {"status" : "error",
             "message" : "Required fields are missing"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try:
        remove_player_from_room(room_id, player_id)
    except Exception as e:
        return Response(
            {"status" : "error",
             "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"status" : "success",
         "message": "Player left the room",
         "room_id" : room_id,
        }
        )
@api_view(["POST"])
def start_game(request):
    room_id = request.data.get("room_id")
    player_id = request.data.get("player_id")
    if room_id is None or player_id is None:
        return Response(
            {"status" : "error",
             "message" : "Required fields are missing"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try:
        start_game_logic(room_id, player_id)
    except Exception as e:
        return Response(
            {"status" : "error",
             "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"status" : "success",
         "message" : "Room started successfully",
         "room_id" : room_id,
        }
    )
@api_view(["POST"])
def select_identity_api(request):
    room_id = request.data.get("room_id")
    player_id = request.data.get("player_id")
    identity = request.data.get("identity")
    if room_id is None or player_id is None or identity is None :
        return Response(
            {
                "status" : "error",
                "message" : "Required fields are missing"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try :
        select_identity_logic(room_id,player_id,identity)
    except ValueError as e :
        return Response(
            {
                "status" : "error",
                "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {
            "status" : "success",
            "message" : "Identity selected successfully ",
            "room_id" : room_id,
            "player_id" : player_id,
            "identity" : identity

        },
        status = status.HTTP_200_OK
    )
@api_view(["POST"])
def complete_identity_api(request):
    room_id = request.data.get("room_id")
    player_id = request.data.get("player_id")
    if room_id is None or player_id is None :
        return Response(
            {
                "status" : "error",
                "message" : "Required fields are missing"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try :
        complete_identity_phase_logic(room_id,player_id)
    except ValueError as e :
        return Response(
            {
                "status" : "error",
                "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {
            "status" : "success",
            "message" : "Identity phase completed",
            "room_id" : room_id

        },
        status = status.HTTP_200_OK
    )
@api_view(["POST"])
def pass_card(request):
    room_id = request.data.get("room_id")
    player_id = request.data.get("player_id")
    card_index = request.data.get("card_index")
    card_index = int(card_index)
    if room_id is None or player_id is None or card_index is None:
        return Response(
            {"status" : "error",
             "message" : "Required fields are missing"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try:
        room = pass_card_logic(room_id,player_id,card_index)
    except ValueError as e:
        return Response(
            {"status" : "error",
             "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"status" : "success",
         "message" : "Card passed successfully",
         "room_state" : room.state
        },
        status = status.HTTP_200_OK
    )
@api_view(["GET"])
def get_player_hand_api(request,room_id,player_id):
    try:
        result = get_player_hand_logic(room_id,player_id)
    except ValueError as e:
        return Response(
            {"status" : "error",
             "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"status" : "success",
         "cards" : result["cards"]
        },
        status = status.HTTP_200_OK
    )
@api_view(["POST"])
def force_finish_round_api(request):
    room_id = request.data.get("room_id")
    if room_id is None:
        return Response(
            {"status" : "error",
             "message" : "Required fields are missing"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try:
        room = force_finish_round_logic(room_id)
    except ValueError as e:
        return Response(
            {"status" : "error",
             "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"status" : "success",
         "message" : "Round finished successfully",
         "room_state" : room.state
        },
        status = status.HTTP_200_OK
    )
@api_view(["POST"]) 
def reset_round_api(request):
    room_id = request.data.get("room_id")
    if room_id is None:
        return Response(
            {"status" : "error",
             "message" : "Required fields are missing"
            },
            status = status.HTTP_400_BAD_REQUEST
        ) 
    try:
        room = reset_round_logic(room_id)
    except ValueError as e:
        return Response(
            {"status" : "error",
             "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"status" : "success",
         "message" : "Round reset completed",
         "room_state" : room.state
        },
        status = status.HTTP_200_OK
    )
@api_view(["POST"])
def participate_in_star_api(request):
    room_id = request.data.get("room_id")
    player_id = request.data.get("player_id")
    if room_id is None or player_id is None:
        return Response(
            {
                "status" : "error",
                "message" : "Required fields are misssing"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try:
        participate_in_star_logic(room_id, player_id)
    except ValueError as e:
        return Response(
            {
                "status" : "error",
                "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return Response(
         {"status" : "success",
          "message" : "Star participation recorded"
         },
         status = status.HTTP_200_OK
    )
@api_view(["POST"])
def set_rounds_api(request):
    room_id = request.data.get("room_id")
    player_id = request.data.get("player_id")
    if room_id is None or player_id is None:
        return Response(
            {"status" : "error",
             "message" : "Required fields are missing"
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try:
        total_rounds = int(total_rounds)
    except ValueError as e:
        return Response(
            {"status" : "error",
             "message" : str(e)
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"status" : "success",
         "message" : "Rounds set successfully",
         "room_id" : room_id,
         "total_rounds" : total_rounds
        },
        status = status.HTTP_200_OK
    )
            