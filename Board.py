import configparser
import Pawn
from Colour import Colour


class Board:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.board_size = int(config['Board_parameters']['BOARD_SIZE'])

    def get_newboard(self):
        # izvieto tukšu 2D sarakstu un izveido tajā esošos pawn objektus.
        # return: 2D  datu struktūra, kas saglabā pawn objektu pozīcijas
        # Šīs koordinātas varat izmantot, lai parādītu kustības1 (move1)

        new_board = [[None for j in range(self.board_size)] for i in range(self.board_size)]
        for i in range(self.board_size // 2 - 1):
            for j in range(0, self.board_size, 2):
                new_board[i][j + i % 2] = Pawn.Pawn(i, j + i % 2, Colour.WHITE.value)
        for i in range(self.board_size // 2 + 1, self.board_size):
            for j in range(0, self.board_size, 2):
                new_board[i][j + i % 2] = Pawn.Pawn(i, j + i % 2, Colour.RED.value)
        return new_board
