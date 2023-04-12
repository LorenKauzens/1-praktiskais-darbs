import configparser
from Colour import Colour
import Pawn
import pygame
from pygame.locals import *
import King
import sys

class Display:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.board_size = int(config['Board_parameters']['BOARD_SIZE'])
        self.window_width = int(config['Window']['WINDOW_WIDTH'])
        self.window_height = int(config['Window']['WINDOW_HEIGHT'])
        self.field_size = int(config['Board_parameters']['FIELD_SIZE'])
        self.displaysurf = pygame.display.set_mode((self.window_width, self.window_height))
        self.xmargin = int((self.window_height - (self.board_size * self.field_size)) / 2)
        self.ymargin = int((self.window_width - (self.board_size * self.field_size)) / 2)
        self.basic_font_size = int(config['Font']['FONT_SIZE'])
        self.basic_font = pygame.font.Font('freesansbold.ttf', self.basic_font_size)

    def get_left_top_of_field(self, fieldy, fieldx):
        # atgriez norādītā lauka kreisās puses X&Y pikseļu koordinātas.

        left_top_Xcoord = (fieldx * self.field_size) + self.ymargin
        left_top_Ycoord = (fieldy * self.field_size) + self.xmargin
        return (left_top_Ycoord, left_top_Xcoord)

    def draw_field(self, fieldy, fieldx):
        # uzzimee taisnu objektu uz virsmas objekta dotajā laukā.

        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
        pygame.draw.rect(self.displaysurf, Colour.BLACK.value, (left_top_Xcoord, left_top_Ycoord, self.field_size, self.field_size))

    def draw_empty_board(self):
        #uzzime objektus uz virsmas objekta, veidojot dambretes deli

        self.displaysurf.fill(Colour.WHITE.value)
        self.board_dim = self.board_size * self.field_size

        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(0, 0)
        pygame.draw.rect(self.displaysurf, Colour.BROWN.value, (left_top_Xcoord, left_top_Ycoord, self.board_dim, self.board_dim))
        counter = 0
        for fieldy in range(self.board_size):
            for fieldx in range(self.board_size):
                if counter % 2 == 0:
                    self.draw_field(fieldy, fieldx)
                counter += 1
            counter += 1

    def draw_pawn(self, fieldy, fieldx, colour):

        half = int(self.field_size * 0.5)

        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
        pygame.draw.circle(self.displaysurf, colour, (left_top_Xcoord + half, left_top_Ycoord + half), half - 5)

    def draw_king_overlay(self, fieldy, fieldx):

        half = int(self.field_size * 0.5)
        quarter = int(self.field_size * 0.25)
        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
        pygame.draw.circle(self.displaysurf, Colour.BLACK.value, (left_top_Xcoord + half, left_top_Ycoord + half), quarter - 5)

    def draw_pieces_on_board(self, board):

        for fieldy in range(len(board)):
            for fieldx in range(len(board[0])):
                if isinstance(board[fieldy][fieldx], Pawn.Pawn):
                    self.draw_pawn(fieldy, fieldx, board[fieldy][fieldx].get_colour())
                elif isinstance(board[fieldy][fieldx], King.King):
                    self.draw_pawn(fieldy, fieldx, board[fieldy][fieldx].get_colour())
                    self.draw_king_overlay(fieldy, fieldx)

    def get_spot_clicked(self, board, mouse_posx, mouse_posy):
        # konverte pikseļu X&Y koordinātas par X&Y koordinātām

        for fieldy in range(len(board)):
            for fieldx in range(len(board)):
                left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
                field_Rect = pygame.Rect(left_top_Xcoord, left_top_Ycoord, self.field_size, self.field_size)
                if field_Rect.collidepoint(mouse_posx, mouse_posy):
                    return fieldy, fieldx
        return None, None

    def draw_highlight(self, fieldy, fieldx):
        # uzzime taisno objektu dotajā laukā, kas kalpo kā lauka robeža.
        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
        pygame.draw.rect(self.displaysurf, Colour.HIGH_LIGHT_COLOUR.value, (left_top_Xcoord, left_top_Ycoord,
                                                                            self.field_size - 3, self.field_size - 3), 4)

    def draw_computer_highlight(self, fieldy, fieldx):
        # uzzime taisno objektu dotajā laukā, kas kalpo kā lauka robeža.
        left_top_Ycoord, left_top_Xcoord = self.get_left_top_of_field(fieldy, fieldx)
        pygame.draw.rect(self.displaysurf, Colour.RED.value, (left_top_Xcoord, left_top_Ycoord,
                                                                           self.field_size - 3, self.field_size - 3), 4)
    def highlight_available_moves(self, available_moves):
        # atkarto pieejamo kustību sarakstu un izsauc metodi draw_highlight() ar patiesajām vērtībām
        for fieldy in range(len(available_moves)):
            for fieldx in range(len(available_moves)):
                if available_moves[fieldy][fieldx] is True:
                    self.draw_highlight(fieldy, fieldx)
        pygame.display.update()

    def update_board(self, board):
        # parbauda  draw_empty_board un draw_pieces_on_board metodes.
        self.draw_empty_board()
        self.draw_pieces_on_board(board)

    def move_piece_animation(self, board, fieldy, fieldx, colour, posy, posx):
        # izsauc metodi draw_pawn/draw_king_overlay pārvietošanas vietā un draw_field metodi figūras atrašanās vietā.

        self.draw_pawn(fieldy, fieldx, colour)
        self.draw_field(posy, posx)
        if isinstance(board[posy][posx], King.King):
            self.draw_king_overlay(fieldy, fieldx)

    def attack_piece_animation(self, board, fieldy, fieldx, colour, posy, posx):
        # izsauc metodi draw_pawn pārvietošanās uzbrukuma galamērķī un draw_field metodi figuras atrašanās vietās.

        attacked_piece_x = int((fieldx + posx) / 2)
        if fieldy < posy:
            attacked_piece_y = posy - 1
        else:
            attacked_piece_y = posy + 1

        self.draw_pawn(fieldy, fieldx, colour)
        if isinstance(board[posy][posx], King.King):
            self.draw_king_overlay(fieldy, fieldx)
        self.draw_field(posy, posx)
        self.draw_field(attacked_piece_y, attacked_piece_x)
        pygame.display.update()

    def victory_animation(self, colour):
        self.displaysurf.fill(colour)
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        import Main  # importe  main_menu module
        Main.main_menu()  # izsauc main() function no main_menu module
        sys.exit()


    def check_for_quit(self):
        # mekle QUIT notikumu ievades un evakuācijas taustiņus un, ja tādi ir, izsauciet, lai pārtrauktu metodi
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            pygame.event.post(event)
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                self.terminate()
            pygame.event.post(event)

    def terminate(self):
        # pabeidz pygame un izsledz programu
        pygame.quit()
        sys.exit()

    def highlight_while_hovering(self, board, display, mouse_clicked, mousey, mousex):
        # izsauc  draw_highlight lodzinus, uz kurām nav noklikšķināts.
        if mouse_clicked is False:
            boxy, boxx = display.get_spot_clicked(board, mousey, mousex)
            if boxy is not None and boxx is not None:
                display.draw_highlight(boxy, boxx)