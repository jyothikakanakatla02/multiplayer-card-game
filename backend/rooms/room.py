from .constants import LOBBY,IDENTITY_SELECTION,IN_GAME,ALL_IDENTITIES,ROUND_OVER,STAR_RACE,ROUND_RESULT
import random
class Room:
    def __init__(self,room_id,host_player):
        self.room_id = room_id
        self.max_players = 7
        self.host_player_id = host_player.player_id
        self.players = []
        self.state = LOBBY
        self.deck = []
        self.star_order = []
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
        identity = identity.strip().capitalize()
        if identity == "":
            raise ValueError("Invalid Identity")
        if identity not in ALL_IDENTITIES :
            raise ValueError("Choose valid Identity from the list")
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
    def generate_deck(self):
        if self.state != IN_GAME :
            raise ValueError("Game not yet started")
        player_identities = []
        for player in self.players :
            player_identities.append(player.identity)
        self.secret_identity = random.choice(player_identities)
        current_deck = []
        for identity in player_identities :
            i = 0
            while i < 4 :
                current_deck.append(
                    {
                        "identity" : identity,
                        "is_secret" : False
                    }
                )
                i += 1
        current_deck.append(
            {
                "identity" : self.secret_identity,
                "is_secret" : True
            }
        )
        random.shuffle(current_deck)
        self.deck = current_deck
    def distribute_cards(self):
        if self.state != IN_GAME:
            raise ValueError("Cards distribution is not allowed yet.")
        if len(self.deck) == 0:
            raise ValueError("Deck is empty")                                                   
        if len(self.deck) != len(self.players)*4 + 1:
            raise ValueError("Deck does not match expected distribution")
        for player in self.players:
            if player.player_id == self.host_player_id:
                cards_to_give = 5 
            else:
                cards_to_give = 4
            for i in range(cards_to_give):
                card = self.deck.pop()
                player.cards.append(card)
        self.current_turn_player_id = self.host_player_id
    def pass_card(self,player_id,card_index):
        if self.state == STAR_RACE:
            raise ValueError("Round already completed")
        if self.state != IN_GAME:
            raise ValueError("Game not in progress")
        if player_id != self.current_turn_player_id:
            raise ValueError("Not your Turn")
        for player in self.players:
            if player.player_id == player_id :
                current_player = player
                break
        else:
            raise ValueError("Player not found")
        if card_index < 0 or card_index >=len(current_player.cards):
            raise ValueError("Invalid card index")
        passed_card = current_player.cards.pop(card_index)
        current_index = self.players.index(current_player)
        next_index = (current_index + 1) % len(self.players)
        next_player = self.players[next_index]
        next_player.cards.append(passed_card)
        self.current_turn_player_id = next_player.player_id
        if len(current_player.cards) == 4 :
            first_card = current_player.cards[0]
            for card in current_player.cards :
                if first_card["identity"] != card["identity"] :
                    break
            else:
                self.round_winner = current_player.player_id
                self.state = STAR_RACE
                self.star_order = []
                return
    def get_player_hand(self,player_id):
        for player in self.players:
            if player.player_id == player_id :
                current_player = player 
                break
        else:
            raise ValueError("Player not found")
        cards_in_hand = [card["identity"] for card in current_player.cards]
        return {
        "cards" : cards_in_hand
        }
    def force_finish_round(self):
        if self.state != STAR_RACE:
            raise ValueError("Invalid state")
        for player in self.players:
            if player.player_id == self.round_winner:
                continue
            if player.player_id in self.star_order:
                continue
            self.star_order.append(player.player_id)
        if len(self.star_order) == len(self.players) - 1:
                self.state = ROUND_OVER
                for player in self.players:
                    if player.player_id == self.round_winner:
                        player.score += 1000
                        break
                player_map = {player.player_id : player for player in self.players}
                for index, player_id in enumerate(self.star_order):
                    player = player_map[player_id]
                    score = 900 - (index * 100)
                    player.score += score
    def reset_round(self):
        self.round_winner = None
        self.star_order = []
        self.state = IDENTITY_SELECTION
        for player in self.players:
            player.cards = []
            player.identity = None
        self.current_turn_player_id = None
        self.secret_identity = None
        self.deck = []
    def participate_in_star(self,player_id):
        if self.state != STAR_RACE :
            raise ValueError ("Invalid Room state")
        if player_id == self.round_winner :
            raise ValueError ("Winner cannot participate in Star Race")
        for player in self.players:
            if player.player_id == player_id :
                current_player = player
                break
        else:
            raise ValueError("Player not found ")
        if player_id in self.star_order:
            raise ValueError ("Player cannot participate in star race twice ")
        self.star_order.append(player_id)
        if len(self.star_order) == len(self.players) - 1:
            self.calculate_scores()
    def calculate_scores(self):
        player_map= {}
        for player in self.players :
            if player.player_id == self.round_winner:
                player.score += 1000
            player_map[player.player_id] = player 
        for index,player_id in enumerate(self.star_order) :
            player = player_map[player_id]
            player.score += 900 - (index * 100)
        self.scores_snapshot = []
        for player in self.players:
            if any(card["is_secret"] for card in player.cards):
                player.score += 100
            self.scores_snapshot.append({
            "nickname" : player.nickname,
            "score" : player.score
            })
        self.state = ROUND_RESULT

