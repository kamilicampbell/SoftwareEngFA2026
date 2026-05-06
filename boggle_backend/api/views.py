# Create your views here.
from __future__ import annotations
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.staticfiles import finders
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .randomGen import random_grid
from .readJSONFile import read_json_to_list
from .boggle_solver import Boggle
from .models import Game, LeaderBoard, LeaderBoardEntry
from .serializers import (
    GameSerializer,
    LeaderBoardEntrySerializer,
    LeaderBoardSerializer,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class CreateGameBySizeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, size: int):
        if size < 3 or size > 10:
            return Response(
                {"detail": "size must be between 3 and 10."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        dictionary_language = request.query_params.get("dictionary", "English")
        try:
            with transaction.atomic():
                grid = random_grid(size)
                now = datetime.now()
                gname = f"Random{size}Grid:{now.strftime('%Y-%m-%d %H:%M:%S')}"
                if dictionary_language.lower() == "spanish":
                    dict_file = "data/spanish-wordlist.json"
                else:
                    dict_file = "data/full-wordlist.json"
                
                file_path = finders.find(dict_file)
                if not file_path:
                    raise Exception(f"Dictionary file not found for language: {dictionary_language}")
                dictionary = read_json_to_list(file_path)
                
                mygame = Boggle(grid, dictionary)
                foundwords = mygame.getSolution()
                normalized = sorted({
                    str(w).strip().upper()
                    for w in foundwords
                    if str(w).strip()
                })
                game = Game.objects.create(
                    name=gname,
                    size=size,
                    grid=grid,
                    dictionary_language=dictionary_language,
                    solution_words=normalized,
                )
                LeaderBoard.objects.create(
                    game=game,
                    title=f"Leaderboard for {game.name}",
                )
            return Response(
                GameSerializer(game).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"detail": f"Game creation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GameListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Game.objects.all().order_by("-date_created")
        return Response(GameSerializer(qs, many=True).data)


class GameDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        game = get_object_or_404(Game, id=id)
        return Response(GameSerializer(game).data)


class GameLeaderBoardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        game = get_object_or_404(Game, id=id)
        leaderboard = getattr(game, "leaderboard", None)
        if leaderboard is None:
            leaderboard = LeaderBoard.objects.create(
                game=game,
                title=f"Leaderboard for {game.name}",
            )
        return Response(LeaderBoardSerializer(leaderboard).data)

    def post(self, request, id):
        game = get_object_or_404(Game, id=id)
        leaderboard = getattr(game, "leaderboard", None)
        if leaderboard is None:
            leaderboard = LeaderBoard.objects.create(
                game=game,
                title=f"Leaderboard for {game.name}",
            )
        serializer = LeaderBoardEntrySerializer(
            data={**request.data, "leaderboard": str(leaderboard.id)},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        if request.user and request.user.is_authenticated:
            user = request.user
        else:
            user_id = serializer.validated_data.pop("user_id")
            user = get_object_or_404(User, id=user_id)
        entry = LeaderBoardEntry.objects.create(
            leaderboard=leaderboard,
            user=user,
            words_found_count=serializer.validated_data.get("words_found_count", 0),
            total_time_seconds=serializer.validated_data.get("total_time_seconds", 0),
        )
        return Response(
            LeaderBoardEntrySerializer(entry).data,
            status=status.HTTP_201_CREATED,
        )


class GameDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id):
        game = get_object_or_404(Game, id=id)
        game.delete()
        return Response(
            {"detail": "Game deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class LeaderBoardEntryDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, id):
        entry = get_object_or_404(LeaderBoardEntry, id=id)
        entry.delete()
        return Response(
            {"detail": "LeaderBoard entry deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already taken."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "username": user.username},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "username": user.username},
            status=status.HTTP_200_OK,
        )
