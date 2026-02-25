import uuid
class Player:
    def __init__(self, nickname, avatar):
        if not isinstance(nickname, str):
            raise ValueError("Nickname must be a string")
        if not isinstance(avatar, str):
            raise ValueError("Avatar must be a string")
        nickname = nickname.strip()
        avatar = avatar.strip()
        if len(nickname) < 3 or len(nickname) > 20:
            raise ValueError("Nickname must be between 3 and 20 characters.")
        if not avatar:
            raise ValueError("Avatar must not be empty.")
        self.nickname = nickname
        self.avatar = avatar
        self.player_id = str(uuid.uuid4())