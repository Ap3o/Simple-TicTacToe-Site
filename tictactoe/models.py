import random
from collections import Counter

from django.db import models
from django.urls import reverse
from django.utils import timezone

from api.models import Notifications


class Game(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)  # созданеи игры
    date_updated = models.DateTimeField(auto_now=True)  # обновление игры

    board = models.CharField(max_length=9, default=" " * 9)  # Доска

    player_x = models.CharField(max_length=64)  # игрок x
    player_o = models.CharField(max_length=64)  # игрок 0
    winner = models.CharField(max_length=1)  # победитель(может быть пустым, если ничья)

    game_ended = models.CharField(max_length=5, default="false")  # закончена игра или нет

    def get_absolute_url(self):
        # метод, отправляющий айди игры
        return reverse('game:detail', kwargs={'pk': self.pk})

    @property
    def next_player(self):
        # Первым всегда ходит X, после ход передается "O"
        count = Counter(self.board)
        if count.get('X', 0) > count.get('O', 0):
            return 'O'
        return 'X'

    # Победные комбинации
    WINNING = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    @property
    def is_game_over(self):
        """
        Метод проверяет, закончилась ли игра.
        В случае победы игрока "X" - отправит "X"
        В случае победы другого игрока, то есть "O", отправит "O"
        В случае, если на поле остались пустые клетки - ответ будет " "
        Если игра завершилась ничьей, ответ будет ' '
        """

        def is_win(board):
            for wins in self.WINNING:
                w = (board[wins[0]], board[wins[1]], board[wins[2]])
                if w == ('X', 'X', 'X'):
                    if self.game_ended == "false":
                        self.send_notify("Вы проиграли игру игру №{0} ".format(
                            self.id) + "против искусственного интеллекта, увы!", "tictactoe-lose")
                    self.game_ended = "true"
                    self.winner = "X"
                    return 'X'
                if w == ('O', 'O', 'O'):
                    if self.game_ended == "false":
                        self.send_notify(
                            "Вы выиграли игру №{0} ".format(self.id) + "против искусственного интеллекта, поздравляем!",
                            "tictactoe-win")
                    self.game_ended = "true"
                    self.winner = "O"
                    return 'O'

        board = list(self.board)
        if self.game_ended == "false":
            if is_win(board) == "O" or is_win(board) == "X":
                return is_win(board)
            if ' ' in board:
                return None
            self.send_notify("Вы сыграли в ничью в игре №{0}".format(self.id), "tictactoe-draw")
            self.game_ended = "true"
            return ' '
        else:
            if is_win(board) is not None:
                return is_win(board)
            else:
                return ' '

    def is_game_end(self):
        # Закончена ли игра, нужно для того, чтобы не было ложных ходов после окончания игры
        if self.is_game_over == "X" or self.is_game_over == "O":
            return True
        else:
            return False

    def play(self, index):
        """
        :param index: -  ход игрока
        :return:
        """

        # обработка исключений, в случае если игрок захочет поменять значения в коде элемента
        if index < 0 or index >= 9:
            raise IndexError("Неправильная клетка")

        if self.board[index] != ' ':
            raise ValueError("Клетка уже занята")

        # Ставим ход игрока на доску
        board = list(self.board)
        board[index] = self.next_player
        self.board = u''.join(board)

    def play_auto(self):
        # метод с рандомным ходом
        while not self.is_game_over:
            next_player = self.next_player
            player = self.player_x if next_player == 'X' else self.player_o
            if player != 'human':
                index = random.randint(0, 8)  # первое значение
                while True:
                    if ' ' in self.board:
                        if self.board[index] != ' ':  # Если значение доски не пустое
                            index = random.randint(0, 8)  # меняем значение
                        else:
                            break
                    else:
                        break
                board = list(self.board)
                board[index] = next_player
                self.board = u''.join(board)
                self.is_game_over
                return
            else:
                return

    def send_notify(self, text, type):
        # метод, отправляющий уведомление об окончании игры
        notify = Notifications(notification_recipient=self.player_o,
                               notification_status="unwatched",
                               notification_header="Крестики-нолики",
                               notification_text=text,
                               notification_time=timezone.now(),
                               notification_type=type
                               )
        notify.save()
