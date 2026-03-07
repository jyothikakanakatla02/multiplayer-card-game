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