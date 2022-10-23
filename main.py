import random

import pygame
import copy
import time
import tetris

pygame.init()

display_width, display_height = 600, 600

display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

empty_board = "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''\n" \
              "''''''''''"

board_info = copy.copy(empty_board)

place_sound = pygame.mixer.Sound("Sounds/Block placed.wav")
theme_song = pygame.mixer.Sound("Sounds/Theme song.mp3")

colors = {"'": (25, 25, 25),  # ' -- empty celL
          "R": (232, 35, 15),  # R -- red
          "G": (62, 191, 29),  # G -- green
          "B": (0, 53, 221),  # B -- blue
          "S": (94, 255, 255),  # S -- sky blue
          "P": (182, 45, 255),  # P -- purple
          "Y": (255, 211, 42),  # Y -- yellow
          "O": (238, 128, 28)}  # O -- orange

I_block = {"color": "S",
           "width": (2, 4, 3, 4),
           "height": (4, 2, 4, 3),
           "dist": (1, 0, 2, 0),
           "states": {1: [(1, 0), (1, 1), (1, 2), (1, 3)],
                      2: [(0, 1), (1, 1), (2, 1), (3, 1)],
                      3: [(2, 0), (2, 1), (2, 2), (2, 3)],
                      4: [(0, 2), (1, 2), (2, 2), (3, 2)]},
           "center": (15, 5)
           }

J_block = {"color": "O",
           "width": (2, 3, 3, 3),
           "height": (3, 2, 3, 3),
           "dist": (0, 0, 1, 0),
           "states": {1: [(1, 0), (1, 1), (1, 2), (0, 2)],
                      2: [(0, 0), (0, 1), (1, 1), (2, 1)],
                      3: [(1, 0), (1, 1), (1, 2), (2, 0)],
                      4: [(0, 1), (1, 1), (2, 1), (2, 2)]},
           "center": (25, 15)
           }

L_block = {"color": "B",
           "width": (3, 3, 2, 3),
           "height": (3, 3, 3, 2),
           "dist": (1, 0, 0, 0),
           "states": {1: [(1, 0), (1, 1), (1, 2), (2, 2)],
                      2: [(0, 2), (0, 1), (1, 1), (2, 1)],
                      3: [(1, 0), (1, 1), (1, 2), (0, 0)],
                      4: [(0, 1), (1, 1), (2, 1), (2, 0)]},
           "center": (5, 15)

           }

S_block = {"color": "G",
           "width": (3, 3, 3, 2),
           "height": (3, 3, 2, 3),
           "dist": (0, 1, 0, 0),
           "states": {1: [(0, 1), (1, 0), (1, 1), (2, 0)],
                      2: [(1, 0), (1, 1), (2, 1), (2, 2)],
                      3: [(0, 2), (1, 1), (1, 2), (2, 1)],
                      4: [(0, 0), (0, 1), (1, 1), (1, 2)]},
           "center": (15, 25)
           }

Z_block = {"color": "R",
           "width": (3, 3, 3, 2),
           "height": (3, 3, 2, 3),
           "dist": (0, 1, 0, 0),
           "states": {1: [(0, 0), (1, 0), (1, 1), (2, 1)],
                      2: [(2, 0), (2, 1), (1, 1), (1, 2)],
                      3: [(0, 1), (1, 1), (1, 2), (2, 2)],
                      4: [(0, 1), (0, 2), (1, 0), (1, 1)]},
           "center": (15, 25)
           }

T_block = {"color": "P",
           "width": (3, 3, 3, 2),
           "height": (3, 3, 2, 3),
           "dist": (0, 1, 0, 0),
           "states": {1: [(0, 1), (1, 0), (1, 1), (2, 1)],
                      2: [(1, 0), (1, 1), (1, 2), (2, 1)],
                      3: [(0, 1), (1, 1), (1, 2), (2, 1)],
                      4: [(0, 1), (1, 0), (1, 1), (1, 2)]},
           "center": (15, 25)
           }

O_block = {"color": "Y",
           "width": (2, 2, 2, 2),
           "height": (2, 2, 2, 2),
           "dist": (0, 0, 0, 0),
           "states": {1: [(0, 0), (0, 1), (1, 0), (1, 1)],
                      2: [(0, 0), (0, 1), (1, 0), (1, 1)],
                      3: [(0, 0), (0, 1), (1, 0), (1, 1)],
                      4: [(0, 0), (0, 1), (1, 0), (1, 1)]},
           "center": (25, 25)
           }


def you_lost_screen(sc):
    g_e = False  # g_e -- game_exit
    dec_made = False  # dec_made -- decision_made
    while not dec_made and not g_e:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g_e = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dec_made = True

        display.fill((50, 50, 50))
        text_to_screen("You lost!", 0, -200, (200, 200, 200), 80)
        text_to_screen(f"Final score: {sc}", 0, -150, (200, 200, 200), 40)
        text_to_screen("Press UP to continue", 0, 10, (200, 200, 200), 50)
        text_to_screen("Or exit", 0, 60, (200, 200, 200), 20)

        clock.tick(100)

        pygame.display.update()

    return dec_made, g_e


def show_next_block(n_b):  # n_b -- next_block
    # (480, 155, 90, 90) -- "next" block properties

    cell_width = 20

    for cell in n_b["states"][1]:
        pygame.draw.rect(display, colors[n_b["color"]], (480 + n_b["center"][0] + cell[0] * cell_width,
                                                         155 + n_b["center"][1] + cell[1] * cell_width,
                                                         cell_width, cell_width),
                         0, 5)


def draw_blocks_on_field(b_i, pos, block, state):
    b_i_list = b_i.split("\n")

    for cell_pos in block["states"][state]:
        row_list = copy.copy(b_i_list[cell_pos[1] + pos[1]])
        row_list = row_list[:(pos[0] + cell_pos[0])] + block["color"] + row_list[(pos[0] + cell_pos[0] + 1):]
        "".join(row_list)

        b_i_list[pos[1] + cell_pos[1]] = row_list

    b_i = "\n".join(b_i_list)

    return b_i, pos


def text_to_screen(text, x_displace, y_displace, color, size):
    font = pygame.font.SysFont("Arial", size)

    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = ((display_width // 2) + x_displace, (display_height // 2) + y_displace)
    display.blit(text, text_rect)


def draw_main_screen(sc, high_sc):  # sc -- score, high_sc -- high_score
    cell_width = 30

    field_width = 10 * cell_width
    field_height = 2 * field_width

    border_color = "#EC8D00"
    field_position = (display_width - field_width) / 2

    display.fill((50, 50, 50))

    pygame.draw.rect(display, border_color, (field_position - 5, -5, field_width + 10, field_height + 5), 5, 1)
    pygame.draw.rect(display, "#0F0F0F", (field_position, -5, field_width, field_height))

    text_to_screen("Next:", 225, -190, (200, 200, 200), 40)
    pygame.draw.rect(display, border_color, (field_position + 325, 150, 100, 100), 5, 1)
    pygame.draw.rect(display, "#0F0F0F", (field_position + 330, 155, 90, 90))

    text_to_screen("Score:", -225, -270, (200, 200, 200), 40)
    text_to_screen(f"{sc}", -225, -220, (200, 200, 200), 40)

    text_to_screen("High", -225, -130, (200, 200, 200), 40)
    text_to_screen("score:", -225, -80, (200, 200, 200), 40)
    text_to_screen(f"{high_sc}", -225, -30, (200, 200, 200), 40)


def board_drawer(b_i, bl_s, pos, cur_b):  # b_i -- board_info, bl_s -- block_state, cur_b -- current_block
    b_i_list = b_i.split("\n")
    for row_counter, row in enumerate(b_i_list):
        for cell_counter, cell in enumerate(row):
            pygame.draw.rect(display, colors[cell],
                             ((cell_counter * 30) + 150, (row_counter * 30) - 155, 30, 30), 0, 5)

    b_i, pos = draw_blocks_on_field(b_i, pos, cur_b, bl_s)

    return b_i


def main_loop(b_i):
    list_of_blocks = [I_block, J_block, L_block, S_block, Z_block, T_block, O_block]

    set_timer = True
    block_fallen = False

    start_time1 = time.time()
    start_time2 = time.time()

    block_pattern = copy.copy(list_of_blocks)
    random.shuffle(block_pattern)
    block_pattern = tetris.shuffle_blocks(block_pattern, list_of_blocks)

    current_block = block_pattern[0]
    block_pattern.pop(0)
    next_block = block_pattern[0]
    falling_period = 0.700

    checked_once = False

    block_pos = [4, 2]
    block_state = 1

    score = 0

    with open("high_score.txt", "r") as file:
        high_score = file.readlines(1)[0]

    game_over = False

    g_e = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g_e = True
                game_over = True

            elif event.type == pygame.KEYDOWN:
                move_keys = [79, 80]

                if event.scancode == 82:
                    start_time2 = time.time()

                    b_i = tetris.erase_block(b_i, current_block, block_pos, block_state)

                    block_state += 1

                    if block_state > 4:
                        block_state = 1

                    if block_pos[0] + current_block["width"][block_state - 1] > 10:
                        block_pos[0] = 10 - current_block["width"][block_state - 1]
                    elif block_pos[0] + current_block["dist"][block_state - 1] < 0:
                        while block_pos[0] + current_block["dist"][block_state - 1] < 0:
                            block_pos[0] += 1

                    while current_block["height"][block_state - 1] + block_pos[1] > 25:
                        block_pos[1] -= 1

                    if tetris.overlap_on_cell(b_i, current_block, block_pos, block_state):
                        block_state -= 1

                    if block_state < 1:
                        block_state = 4

                elif event.scancode in move_keys:
                    b_i = tetris.erase_block(b_i, current_block, block_pos, block_state)

                    if event.scancode == 79:
                        if block_pos[0] + current_block["width"][block_state - 1] >= 10:
                            pass
                        else:
                            if not tetris.overlap_on_cell(b_i, current_block, (block_pos[0] + 1, block_pos[1]),
                                                          block_state):
                                block_pos[0] += 1
                                start_time2 = time.time()

                    elif event.scancode == 80:
                        if block_pos[0] + current_block["dist"][block_state - 1] <= 0:
                            pass
                        else:
                            if not tetris.overlap_on_cell(b_i, current_block, (block_pos[0] - 1, block_pos[1]),
                                                          block_state):
                                block_pos[0] -= 1
                                start_time2 = time.time()

                elif event.scancode == 81:
                    b_i = tetris.erase_block(b_i, current_block, block_pos, block_state)
                    if not tetris.blocks_beneath(current_block, block_pos, block_state, b_i):
                        block_pos[1] += 1
                        start_time1 = time.time()

        if set_timer:
            b_i = tetris.erase_block(b_i, current_block, block_pos, block_state)
            block_pos[1] += 1

        draw_main_screen(score, high_score)

        show_next_block(next_block)

        b_i = board_drawer(b_i, block_state, block_pos, current_block)

        if tetris.blocks_beneath(current_block, block_pos, block_state, b_i):
            start_time1 = time.time()
            if not checked_once:
                start_time2 = time.time()
            checked_once = True
            block_fallen, start_time2 = tetris.timer(block_fallen, start_time2, 0.25)
            if block_fallen:
                checked_once = False
                block_fallen = False

                b_i, score = tetris.clear_full_lines(b_i, score)

                block_pos = [4, 2]

                current_block = next_block
                block_pattern.pop(0)
                next_block = block_pattern[0]

                if len(block_pattern) <= 7:
                    block_pattern = tetris.shuffle_blocks(block_pattern, list_of_blocks)

                falling_period -= 0.001  # increase falling speed (difficulty)

                block_state = 1
                game_over = tetris.overlap_on_cell(b_i, current_block, block_pos, block_state)

                place_sound.set_volume(0.1)
                place_sound.play()

        set_timer, start_time1 = tetris.timer(set_timer, start_time1, falling_period)

        clock.tick(100)

        pygame.display.update()

    if int(high_score) < score:
        with open("high_score.txt", "r+") as file:
            file.truncate()
            file.write(f"{score}")

    return score, g_e


theme_song.set_volume(0.4)
theme_song.play(-1)

scr, game_exit = main_loop(board_info)
decision_made = False

while not game_exit:
    if decision_made:
        decision_made = False
        scr, game_exit = main_loop(board_info)  # scr -- score

    if not game_exit:
        decision_made, game_exit = you_lost_screen(scr)
