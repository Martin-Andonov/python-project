import pygame
import sys
import tkinter

gray_2 = (155, 155, 155)
gray = (55, 55, 55)
pink = (100, 0, 100)
red = (155, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)


def game_start():

    pygame.init()
    surface_init = pygame.display.set_mode((800, 700))
    return surface_init


def win_check(red_list, yellow_list):
    diagonal_check_1 = [0, 1, 2, 3, 7, 8, 9, 10, 14, 15, 16, 17]
    diagonal_check_2 = [3, 4, 5, 6, 10, 11, 12, 13, 17, 18, 19, 20]
    diagonal_check_3 = [24, 25, 26, 27, 31, 32, 33, 34, 38, 39, 40, 41]
    diagonal_check_4 = [21, 22, 23, 24, 28, 29, 30, 31, 35, 36, 37, 38]
    pygame.display.update()
    counter = 0

    '''horizontal checks'''
    for i in range(42):
        if i in red_list:
            counter += 1
        else:
            counter = 0

        if i % 7 == 0:
            counter = 0

        if counter >= 4:
            win("Red")

    counter = 0

    for i in range(42):
        if i in yellow_list:
            counter += 1
        else:
            counter = 0

        if i % 7 == 0:
            counter = 0

        if counter >= 4:
            win("yellow")

    '''vertical check'''
    for i in red_list:
        if i in red_list and i + 7 in red_list and i + 14 in red_list and i + 21 in red_list and i + 21 < 42:
            win("Red")

    for i in yellow_list:
        if i + 21 < 42:
            if i in yellow_list and i + 7 in yellow_list and i + 14 in yellow_list and i + 21 in yellow_list:
                win("Yellow")

    '''diagonal_checks'''
    for element in diagonal_check_1:
        if element in red_list and element + 8 in red_list and element + 16 in red_list and element + 24 in red_list:
            win("Red")
        if element in yellow_list and element + 8 in yellow_list and element + 16 in yellow_list and element + 24 in yellow_list:
            win("Yellow")
    for element in diagonal_check_2:
        if element in red_list and element + 6 in red_list and element + 12 in red_list and element + 18 in red_list:
            win("Red")
        if element in yellow_list and element + 6 in yellow_list and element + 12 in yellow_list and element + 18 in yellow_list:
            win("Yellow")

    for element in diagonal_check_3:
        if element in red_list and element - 8 in red_list and element - 16 in red_list and element - 24 in red_list:
            win("Red")
        if element in yellow_list and element - 8 in yellow_list and element - 16 in yellow_list and element - 24 in yellow_list:
            win("Yellow")
    for element in diagonal_check_4:
        if element in red_list and element - 6 in red_list and element - 12 in red_list and element - 18 in red_list:
            win("Red")
        if element in yellow_list and element - 6 in yellow_list and element - 12 in yellow_list and element - 18 in yellow_list:
            win("Yellow")


def draw_check(clicked_sprites):
    pygame.display.update()
    if sum(clicked_sprites) == 861:
        draw()


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
    circles = []
    shadows = []
    red_list = []
    yellow_list = []
    clicked_sprites = []
    append_number = 0
    surface.fill(gray)
    player_turn = 2
    y = 70

    for j in range(6):
        x = 70
        for i in range(7):
            shadows.append(pygame.draw.circle(surface, gray_2, (x, y), 50))
            x += 110
        y += 110

    y = 70

    for j in range(6):
        x = 70
        for i in range(7):
            circles.append(pygame.draw.circle(surface, white, (x, y), 45))
            x += 110
        y += 110

    pygame.display.update()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:

                pos = pygame.mouse.get_pos()
                for i in range(42):
                    if circles[i].collidepoint(pos) and i not in clicked_sprites:
                        clicked_row = i
                        while clicked_row < 42:
                            if clicked_row in clicked_sprites:
                                pass
                            else:
                                append_number = clicked_row

                            clicked_row += 7

                        clicked_sprites.append(append_number)

                        x = circles[append_number].x + 45
                        y = circles[append_number].y + 45

                        if player_turn % 2 == 0:

                            shadows[append_number] = pygame.draw.circle(surface, gray, (x, y), 50)
                            circles[append_number] = pygame.draw.circle(surface, red, (x, y), 45)
                            red_list.append(append_number)
                            player_turn += 1

                        else:
                            shadows[append_number] = pygame.draw.circle(surface, gray, (x, y), 50)
                            circles[append_number] = pygame.draw.circle(surface, yellow, (x, y), 45)
                            yellow_list.append(append_number)
                            player_turn += 1

                        pygame.display.update()
                    elif circles[i].collidepoint(pos) and i in clicked_sprites:

                        clicked_row = i
                        while clicked_row > 0:

                            clicked_row -= 7

                            if clicked_row not in clicked_sprites and clicked_row >= 0:

                                append_number = clicked_row

                                clicked_sprites.append(clicked_row)

                                x = circles[append_number].x + 45
                                y = circles[append_number].y + 45

                                if player_turn % 2 == 0:

                                    shadows[append_number] = pygame.draw.circle(surface, gray, (x, y), 50)
                                    circles[append_number] = pygame.draw.circle(surface, red, (x, y), 45)
                                    red_list.append(append_number)
                                    player_turn += 1

                                else:
                                    shadows[append_number] = pygame.draw.circle(surface, gray, (x, y), 50)
                                    circles[append_number] = pygame.draw.circle(surface, yellow, (x, y), 45)
                                    yellow_list.append(append_number)
                                    player_turn += 1

                                pygame.display.update()
                                break

                print(clicked_sprites)

                win_check(red_list, yellow_list)
                draw_check(clicked_sprites)

        pass

    pass


main()
