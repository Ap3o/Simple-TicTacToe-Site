from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from api.models import Notifications
from .forms import NewGameForm, PlayForm
from .models import Game


# Create your views here.

@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        form = NewGameForm(request.POST)
        if form.is_valid():

            # Есть ли начатая игра
            is_game_started = Game.objects.filter(player_o=request.user.id, game_ended="false").values()
            print(is_game_started)
            if len(is_game_started) != 0:
                # Если есть, игрока перекинет на начатую ранее игру.
                return redirect("/game/" + str(is_game_started[0]['id']))

            game = form.create()
            # Пускай первым ходит компьютер. Сразу же сохраняем его ход и присылаем уведомление о начале игры
            game.play_auto()
            game.save()
            send_notify = Notifications(notification_recipient=request.user.id,
                                        notification_status="unwatched",
                                        notification_header="Крестики-нолики",
                                        notification_text="Вы начали игру №{0} ".format(
                                            game.id) + "против искусственного интеллекта, удачи!",
                                        notification_time=timezone.now(),
                                        notification_type="game-start"
                                        )
            send_notify.save()
            return redirect(game)
    else:
        form = NewGameForm()
    matches = Game.objects.filter(player_o=request.user.id)
    wins = len(matches.filter(winner="O").values())
    draws = len(matches.filter(winner='').values())
    matches = len(matches.values())
    loses = matches - wins - draws
    return render(request, 'game/game_main.html',
                  {'form': form, 'matches': matches, 'loses': loses, 'wins': wins, 'draws': draws})


@login_required(login_url="/login/")
@require_http_methods(["GET", "POST"])
def game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == "POST":
        form = PlayForm(request.POST)
        # если другой пользователь зайдет в Вашу игру и попытается сыграть там
        if str(request.user.id) != str(game.player_o):
            return render(request, "game/game_second.html", {
                'game': game, 'error': 'Не вы играете в этой партии!'})

        if form.is_valid():
            # Статус игры, чтобы не делать ложных ходов
            if game.game_ended == "false":
                game_status = False
            else:
                game_status = True
            game.play(form.cleaned_data['index'])
            game.play_auto()
            if not game_status:
                game.save()
            # По-хорошему тут надо бы сделать ajax запрос, но что-то мне помешало это сделать.
            return redirect(game)
    return render(request, "game/game_second.html", {
        'game': game
    })
