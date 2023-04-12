from Piece import Piece
from Colour import Colour
from King import King
import configparser


class Pawn(Piece):
    def __init__(self, posy, posx, colour):
        # Bandinieku klases konstruktors.

        super().__init__(posy, posx, colour)
        if self.colour == Colour.WHITE.value:
            self.direction = -1
        else:
            self.direction = 1
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.board_size = int(config['Board_parameters']['BOARD_SIZE'])

    def is_valid_attack(self, board, fieldy, fieldx):
        # parbauda vai uzbrukums bija valid
        piece_position_y = self.posy - self.direction
        piece_position_x = int((self.posx + fieldx) / 2)
        if abs(self.posx - fieldx) == 2 and self.posy - fieldy == 2 * self.direction and not isinstance(board[fieldy][fieldx], Piece):
            if isinstance(board[piece_position_y][piece_position_x], Piece) and board[piece_position_y][piece_position_x].get_colour() != self.colour:
                return True
            else:
                return False
        else:
            return False

    def attack_piece(self, board, fieldy, fieldx):
        # atjauno dambretes  datu struktūru un gabala posy,posx atribūtus atbilstoši veiktajam uzbrukumam.
        attacked_piece_position_y = self.posy - self.direction
        attacked_piece_position_x = int((self.posx + fieldx) / 2)
        board[attacked_piece_position_y][attacked_piece_position_x] = None

        board[self.posy][self.posx], board[fieldy][fieldx] = board[fieldy][fieldx], board[self.posy][self.posx]
        self.posy = fieldy
        self.posx = fieldx

    def promote_pawn(self, board):
        #Instantiēt King klases objektu.
        board[self.posy][self.posx] = King(self.posy, self.posx, self.colour)

    def check_for_promotion(self, board):
        # parbauda, vai ir pieejams paaugstinājums, un, ja ir, izsauc metodi promote_pawn.

        if self.posy == self.board_size - 1 and self.colour is Colour.WHITE.value:
            self.promote_pawn(board)
        elif self.posy == 0 and self.colour is Colour.RED.value:
            self.promote_pawn(board)




