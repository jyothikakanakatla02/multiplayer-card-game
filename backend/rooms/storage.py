from .room import Room
from .constants import LOBBY,IN_GAME
import random
import string
active_rooms = {}
def _generate_room_id():
    character_pool = string.ascii_uppercase + string.digits
    room_id = "".join(random.choice(character_pool) for _ in range(8))
    while room_id in active_rooms:
        room_id = "".join(random.choice(character_pool) for _ in range(8))
    return room_id
def create_room(host_player):
    room_id = _generate_room_id()
    room = Room(room_id,host_player)
    active_rooms[room_id] = room
    return room_id
def add_player_to_room(room_id,player):
    if room_id not in active_rooms:
        raise ValueError("Room not found")
    room = active_rooms[room_id]
    room.add_player(player)
def get_room(room_id):
    room = active_rooms.get(room_id)
    if room is None:
        raise ValueError("Room not found")
    return room
def remove_player_from_room(room_id, player_id):
    if room_id not in active_rooms:
        raise ValueError("Room not found")
    room = active_rooms[room_id]
    for player in room.players:
        if player.player_id == player_id:
            room.players.remove(player)
            break
    else:
        raise ValueError("player not found")
    if len(room.players) == 0:
        del active_rooms[room_id]
    elif room.host_player_id == player_id :
        room.host_player_id = room.players[0].player_id
    
def start_game_logic(room_id,player_id):
    room = get_room(room_id)
    if room is None:
        raise ValueError("Room not Found")
    if player_id != room.host_player_id :
        raise ValueError("Only Host can start the Game")
    if room.state != LOBBY:
        raise ValueError("Game already started")
    if len(room.players) < 3 :
        raise ValueError("Not enough players")
    room.state = IN_GAME
    return room
