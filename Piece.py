from Colour import Colour


class Piece:
    def __init__(self, posy, posx, colour):
        self.posy = posy
        self.posx = posx
        self.colour = colour

        if self.colour == Colour.WHITE.value:
            self.direction = -1
        else:
            self.direction = 1

    def get_colour(self):
        #  atgriez krasas atributa vertibas
        return self.colour

    def get_available_moves(self, board):
        #  dambretes apakšsarakst izsauc metodi is_valid_move un pievieno tās atgriešanas vērtības sarakstam.

        available_moves = []
        for fieldx in range(len(board)):
            column = []
            for fieldy in range(len(board)):
                legit_move = board[self.posy][self.posx].is_valid_move(board, fieldx, fieldy)
                column.append(legit_move)
            available_moves.append(column)
        return available_moves

    def get_available_attacks(self, board):
        #atkartoti izmanto  apakšsarakstu un izsauc metodi is_valid_attack un pievieno tās atgriešanas vērtības sarakstam


        available_attacks = []
        for fieldx in range(len(board)):
            column = []
            for fieldy in range(len(board)):
                legit_attack = board[self.posy][self.posx].is_valid_attack(board, fieldx, fieldy)
                column.append(legit_attack)
            available_attacks.append(column)
        return available_attacks

    def get_all_available_moves(self, board):
        # atgriez available_attacks un uzbrūk, ja tādi ir, pretējā gadījumā atgriez available_moves un False uzbrukuma vērtību

        available_attacks = self.get_available_attacks(board)
        if any(True in sublist for sublist in available_attacks):
            attack = True
            return available_attacks, attack
        else:
            available_moves = self.get_available_moves(board)
            attack = False
            return available_moves, attack

    def is_valid_move(self, board, fieldy, fieldx):
        # parbauda vai kustiba dotaja lokacija ir valid/deriga

        if isinstance(board[fieldy][fieldx], Piece):
            return False
        if self.posy - fieldy == self.direction and abs(self.posx - fieldx) == 1:
            return True
        else:
            return False

    def make_move(self, board, fieldy, fieldx):
        # atjaunina dambretes datu struktūru un gabala atribūtus, kas ir atbildīgi par tā atrašanās vietu.

        board[self.posy][self.posx], board[fieldy][fieldx] = board[fieldy][fieldx], board[self.posy][self.posx]
        self.posy = fieldy
        self.posx = fieldx

    def can_piece_attack(self, board):
        available_attacks = []
        for fieldx in range(len(board)):
            column = []
            for fieldy in range(len(board)):
                legit_attack = board[self.posy][self.posx].is_valid_attack(board, fieldx, fieldy)
                column.append(legit_attack)
            available_attacks.append(column)

        if any(True in sublist for sublist in available_attacks):
            return True
        else:
            return False
