from .room import Room
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

