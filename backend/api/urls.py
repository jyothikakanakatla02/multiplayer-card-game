from django.urls import path
from .views import join_room
urlpatterns = [
    path("join-room/", join_room, name="join-room")
]