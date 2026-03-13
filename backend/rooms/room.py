from .constants import LOBBY,IDENTITY_SELECTION,IN_GAME,ALL_IDENTITIES
import random
class Room:
    def __init__(self,room_id,host_player):
        self.room_id = room_id
        self.max_players = 7
        self.host_player_id = host_player.player_id
        self.players = []
        self.state = LOBBY
        self.add_player(host_player)
    def add_player(self,player):
        if self.state != LOBBY:
            raise ValueError("Game already started")
        if len(self.players) >= self.max_players:
            raise ValueError("Room is Full")
        for existing_player in self.players:
            if existing_player.nickname == player.nickname:
                raise ValueError("Nickname already taken, Please choose another nickname")
        self.players.append(player)
    def select_identity(self, player_id, identity):
        if self.state != IDENTITY_SELECTION:
            raise ValueError("Identity selection is not allowed right now")
        found_player = None
        for player in self.players:
            if player.player_id == player_id:
                found_player = player
                if player.identity is not None:
                    raise ValueError("You cannot choose identity again")
        if found_player is None:
            raise ValueError("Player not found in the room") 
        for existing_player in self.players:
            if existing_player.identity == identity:
                raise ValueError("Identity already taken")
        found_player.identity = identity
        for player in self.players:
            if player.identity is None:
                return    
        self.state = IN_GAME 
    def complete_identity_phase(self):
        if self.state != IDENTITY_SELECTION:
            raise ValueError("Identity phase is not active")
        players_without_identity = []
        used_identities = []
        for player in self.players:
            if player.identity is None:
                players_without_identity.append(player)
            else:
                used_identities.append(player.identity)
        unused_identities = []
        for identity in ALL_IDENTITIES:
            if identity not in used_identities:
                unused_identities.append(identity)
        for player in players_without_identity:
            identity = random.choice(unused_identities)
            player.identity = identity
            unused_identities.remove(identity)
        self.state = IN_GAME
        



                