from django import forms

from .models import Game


class NewGameForm(forms.Form):
    # крестик
    player1 = forms.CharField(max_length=64, required=True,
                              validators=[])

    # нолик
    player2 = forms.CharField(max_length=64, required=True,
                              validators=[])

    def create(self):
        # Создание игры
        players = [self.cleaned_data['player1'], self.cleaned_data['player2']]
        # random.shuffle(players) пока отказался от перемешивания
        return Game.objects.create(player_x=players[1],
                                   player_o=players[0])


class PlayForm(forms.Form):
    index = forms.IntegerField(min_value=0, max_value=8)
