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
from rooms.storage import add_player_to_room
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
