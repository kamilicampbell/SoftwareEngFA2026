from django.urls import path
from .views import (
    CreateGameBySizeView,
    GameListView,
    GameDetailView,
    GameLeaderBoardView,
    GameDeleteView,
    LeaderBoardEntryDeleteView,
)

urlpatterns = [
    path("game/<int:size>/", CreateGameBySizeView.as_view(), name="create-game-by-size"),
    path("games/", GameListView.as_view(), name="game-list"),
    path("games/<uuid:id>/", GameDetailView.as_view(), name="game-detail"),
    path("games/<uuid:id>/leaderboard/", GameLeaderBoardView.as_view(), name="game-leaderboard"),
    path("games/<uuid:id>/delete/", GameDeleteView.as_view(), name="game-delete"),
    path("leaderboard/entries/<uuid:id>/delete/", LeaderBoardEntryDeleteView.as_view(), name="leaderboard-entry-delete"),
]
