from players.player import Player
from rooms.storage import create_room
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
from rooms.storage import add_player_to_room, remove_player_from_room, start_game_logic, select_identity_logic
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
    players_data = []
    for player in room.players:
        if player.player_id == room.host_player_id:
            is_host = True
        else:
            is_host = False
        players_data.append({"nickname":player.nickname,
                             "avatar": player.avatar,
                             "is_host" : is_host})
    return Response({
        "status" : "success",
        "room_id" : room_id,
        "total_players" : len(players_data),
        "players" : players_data
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
def select_identity(request):
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
