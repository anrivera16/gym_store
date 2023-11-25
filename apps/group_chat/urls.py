from django.urls import path

from . import views

app_name = "group_chat"

urlpatterns = [
    path("", views.chat_list, name="chat_list"),
    path("<str:room_name>/", views.chat_room, name="chat_room"),
]
