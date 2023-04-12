import pygame, sys
from Player import Player
from Colour import Colour
from GameLogic import main

# uzsak pygame
pygame.init()

def main_menu():
    ai_player = Player(Colour.WHITE.value, False)
    human_player = Player(Colour.RED.value, True)
    game_on = True
    moves = []

    # iestata displaju
    screen = pygame.display.set_mode((480, 600))
    menu_font = pygame.font.Font(None, 80)
    menu_text_surface = menu_font.render("MENU", True, (255, 255, 255))
    screen.blit(menu_text_surface, (150, 60))

    button_rect_one = pygame.Rect(135, 200, 200, 50)
    pygame.draw.rect(screen, (154, 42, 42), button_rect_one, border_radius=10)
    font = pygame.font.Font(None, 30)
    text_surface = font.render("Player Start!", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect_one.center)
    screen.blit(text_surface, text_rect)

    button_rect_two = pygame.Rect(135, 280, 200, 50)
    pygame.draw.rect(screen, (255, 255, 255), button_rect_two, border_radius=10)
    text_surface = font.render("Computer Start!", True, (154, 42, 42))
    text_rect = text_surface.get_rect(center=button_rect_two.center)
    screen.blit(text_surface, text_rect)

    button_quit = pygame.Rect(175, 400, 120, 50)
    pygame.draw.rect(screen, (154, 42, 42), button_quit, border_radius=10)
    text_surface = font.render("Quit!", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=button_quit.center)
    screen.blit(text_surface, text_rect)

    # atjauno displaju
    pygame.display.flip()

    # speles loop
    while game_on:
        # apstrada visu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #  parbauda vai peles klikskis bija pogas tainsturi
                if button_rect_one.collidepoint(event.pos):
                    moves = main(human_player, ai_player)
                elif button_rect_two.collidepoint(event.pos):
                    human_player.turn = False
                    ai_player.turn = True
                    moves = main(human_player, ai_player)
                elif button_quit.collidepoint(event.pos):
                    game_on = False

        # uztaisa movse kur katrs rada ka dators vai cilveks kustejas
        screen.fill((0, 0, 0), (0, 470, 480, 130))
        font = pygame.font.Font(None, 24)
        text = "Moves:"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 480))
        for i, move in enumerate(moves):
            text_surface = font.render(move, True, (255, 255, 255))
            screen.blit(text_surface, (10, 500 + i * 20))

        # atjauno displayu
        pygame.display.flip()

if __name__ == '__main__':
    main_menu()