import random
import copy
import time
import pygame


def shuffle_blocks(l1, l_of_b):  # l_of_b -- list_of_blocks
    random.shuffle(l_of_b)
    list2 = copy.copy(l_of_b)

    for b in list2:
        l1.append(b)

    return l1


def combo(len_of_clr_row):  # len_of_clr_row -- length_of_cleared_rows (length of list)
    return ((len_of_clr_row**2)/2) + (len_of_clr_row/2)


def overlap_on_cell(b_i, block, pos, state):
    b_i_list = b_i.split("\n")
    s_on_c = False  # s_on_c -- spawned_on_cell

    cells_pos = block["states"][state]

    for cell_pos in cells_pos:
        if b_i_list[cell_pos[1] + pos[1]][cell_pos[0] + pos[0]] != "'":
            s_on_c = True
            break

    return s_on_c


def clear_full_lines(b_i, sc):  # sc -- score
    b_i_list = b_i.split("\n")
    cleared_rows = []

    for row_counter, row in enumerate(b_i_list):
        if "'" in row:
            pass
        else:
            cleared_rows.append(row_counter)

    sc += int(combo(len(cleared_rows)) * 10)

    if len(cleared_rows) > 0:
        pygame.mixer.Sound("Sounds/cleared.aiff").set_volume(0.5)
        pygame.mixer.Sound("Sounds/cleared.aiff").play()

    for row_index in cleared_rows:
        b_i_list.pop(row_index)
        b_i_list.insert(0, "''''''''''")

    b_i = "\n".join(b_i_list)

    return b_i, sc


def find_the_lowest_cells(block, state):
    cells_pos = block["states"][state]
    list0 = []
    list1 = []
    list2 = []
    list3 = []

    lowest_points = []

    for cell_pos in cells_pos:
        if cell_pos[0] == 0:
            list0.append(cell_pos)
        elif cell_pos[0] == 1:
            list1.append(cell_pos)
        elif cell_pos[0] == 2:
            list2.append(cell_pos)
        elif cell_pos[0] == 3:
            list3.append(cell_pos)

    lowest_cell_pos = (0, 0)

    for cell_pos in list0:
        if cell_pos[1] > lowest_cell_pos[1]:
            lowest_cell_pos = cell_pos

    if lowest_cell_pos != (0, 0) or (0, 0) in list0:
        lowest_points.append(lowest_cell_pos)

    lowest_cell_pos = (0, 0)

    for cell_pos in list1:
        if cell_pos[1] >= lowest_cell_pos[1]:
            lowest_cell_pos = cell_pos

    if lowest_cell_pos != (0, 0):
        lowest_points.append(lowest_cell_pos)
    lowest_cell_pos = (0, 0)

    for cell_pos in list2:
        if cell_pos[1] >= lowest_cell_pos[1]:
            lowest_cell_pos = cell_pos

    if lowest_cell_pos != (0, 0):
        lowest_points.append(lowest_cell_pos)
    lowest_cell_pos = (0, 0)

    for cell_pos in list3:
        if cell_pos[1] >= lowest_cell_pos[1]:
            lowest_cell_pos = cell_pos

    if lowest_cell_pos != (0, 0):
        lowest_points.append(lowest_cell_pos)

    return lowest_points


def blocks_beneath(block, pos, state, b_i):
    l_p = find_the_lowest_cells(block, state)  # l_p -- lowest_points
    b_i_list = b_i.split("\n")
    stop_falling = False

    for cell_pos in l_p:

        if cell_pos[1] + pos[1] < 24:
            row_list = copy.copy(b_i_list[cell_pos[1] + pos[1] + 1])
            if row_list[pos[0] + cell_pos[0]] != "'":
                stop_falling = True
            "".join(row_list)

        else:
            stop_falling = True

    return stop_falling


def timer(indicator, sr_t, duration):  # sr_t -- start_timer
    current_time = time.time()

    if current_time - sr_t > duration + 1:
        sr_t = time.time()
    if indicator:
        indicator = False
        sr_t = time.time()

    if current_time - sr_t > duration:
        indicator = True

    return indicator, sr_t


def erase_block(b_i, block, pos, state):
    b_i_list = b_i.split("\n")

    for cell_pos in block["states"][state]:
        row_list = copy.copy(b_i_list[cell_pos[1] + pos[1]])
        row_list = row_list[:(pos[0] + cell_pos[0])] + "\'" + row_list[(pos[0] + cell_pos[0] + 1):]
        "".join(row_list)

        b_i_list[pos[1] + cell_pos[1]] = row_list

    b_i = "\n".join(b_i_list)

    return b_i