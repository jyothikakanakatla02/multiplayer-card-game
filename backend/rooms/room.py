class Room:
    def __init__(self,room_id,host_player):
        self.room_id = room_id
        self.max_players = 7
        self.host_player_id = host_player.player_id
        self.players = []
        self.add_player(host_player)
    def add_player(self,player):
        if len(self.players) >= self.max_players:
            raise ValueError("Limit Exceeded")
        for existing_player in self.players:
            if existing_player.nickname == player.nickname:
                raise ValueError("Nickname already taken, Please choose another nickname")
        self.players.append(player)