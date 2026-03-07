from django.urls import path
<<<<<<< HEAD
from .views import create_room_view,join_room
urlpatterns = [
    path("create-room/", create_room_view),
    path("join-room/", join_room, name="join-room")
]

=======
from .views import join_room
urlpatterns = [
    path("join-room/", join_room, name="join-room")
]
>>>>>>> 3148ab1bdd29f6257ef0fc56d2deaf8eb90815ea
