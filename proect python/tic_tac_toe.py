import pygame
import sys
import tkinter

gray = (55, 55, 55)
gray_2 = (155, 155, 155)
white = (255, 255, 255)
green_blue = (0, 120, 120)
pink = (155, 0, 55)
black = (0, 0, 0)


def game_start():

    pygame.init()
    surface_init = pygame.display.set_mode((345, 345))
    return surface_init


def win_check(x_list, o_list):

    win_conditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [6, 4, 2]]
    counter = 0

    for lists in win_conditions:
        for items in lists:
            if items in x_list:
                counter += 1
            else:
                counter = 0
                break
        if counter > 0:
            win("X")

    for lists in win_conditions:
        for items in lists:
            if items in o_list:
                counter += 1
            else:
                counter = 0
                break
        if counter > 0:
            win("O")


def win(string):
    print_string = string + " won the game!!!"

    root = tkinter.Tk()
    root.eval('tk::PlaceWindow . center')
    root.title("WINNER")

    window = tkinter.Text(root, height=2, width=30)
    window.insert(tkinter.END, print_string)
    window.configure(state='disabled')
    window.pack()

    tkinter.mainloop()

    quit()


def draw_check(clicked_sprites):

    draw_conditions = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    counter = 0

    for items in draw_conditions:
        if items in clicked_sprites:
            counter += 1
        else:
            counter = 0
            break

    if counter > 0:
        draw()


def draw():

    root = tkinter.Tk()
    root.eval('tk::PlaceWindow . center')
    root.title("DRAW")

    window = tkinter.Text(root, height=2, width=30)
    window.insert(tkinter.END, "DRAW!!!")
    window.configure(state='disabled')
    window.pack()

    tkinter.mainloop()

    quit()


def main():

    surface = game_start()
    clicked_sprites = []
    squares = []
    shadows = []
    x_list = []
    o_list = []
    player_turn = 0
    font = pygame.font.Font('freesansbold.ttf', 70)
    x_text = font.render('X', True, gray, green_blue)
    o_text = font.render('O', True, gray, pink)

    surface.fill(gray)

    x = 25
    for i in range(3):
        y = 25
        for j in range(3):
            shadows.append(pygame.draw.rect(surface, gray_2, pygame.Rect(x, y, 85, 85)))
            y += 105
        x += 105

    x = 30
    for i in range(3):
        y = 30
        for j in range(3):
            squares.append(pygame.draw.rect(surface, white, pygame.Rect(x, y, 75, 75)))
            y += 105
        x += 105

    while True:

        win_check(x_list, o_list)
        draw_check(clicked_sprites)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for i in range(9):
                    if squares[i].collidepoint(pos) and i not in clicked_sprites:

                        clicked_sprites.append(i)
                        x = squares[i].x
                        y = squares[i].y

                        if player_turn % 2 == 0:
                            shadows[i] = pygame.draw.rect(surface, gray, pygame.Rect(x - 5, y - 5, 85, 85))
                            squares[i] = pygame.draw.rect(surface, green_blue, pygame.Rect(x, y, 75, 75))

                            text_rect = x_text.get_rect()
                            text_rect.center = (x + 37, y + 40)
                            surface.blit(x_text, text_rect)

                            x_list.append(i)
                        else:
                            shadows[i] = pygame.draw.rect(surface, gray, pygame.Rect(x - 5, y - 5, 85, 85))
                            squares[i] = pygame.draw.rect(surface, pink, pygame.Rect(x, y, 75, 75))

                            text_rect = o_text.get_rect()
                            text_rect.center = (x + 37, y + 40)
                            surface.blit(o_text, text_rect)

                            o_list.append(i)

                        player_turn += 1

                # print(clicked_sprites)

        pygame.display.update()


main()
