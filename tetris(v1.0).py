import pygame
import random

pygame.init()
window = pygame.display.set_mode((700, 800))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
frame_count = 0

menu = True
pause_menu = False
game_over = False

piece_list = ["i", "j", "l", "o", "s", "t", "z"]
speed = 48
fast_drop = False
bottom_frame = 0
switch_ready = False
held_piece = None
piece_held = False
recent_piece_hold = False
score = 0
level = 0
total_lines = 0
required_lines = 10
touching_bottom = False

white = (255, 255, 255)
gray = (128, 128, 128)

light_blue = (0, 255, 255)  # for i block
blue = (0, 0, 255)  # for j block
orange = (255, 165, 0)  # for l block
yellow = (255, 255, 0)  # for o block
green = (0, 255, 0)  # for s block
purple = (128, 0, 128)  # for t block
red = (255, 0, 0)  # for z block

title_font = pygame.font.SysFont("Times New Roman", 70)
menu_font = pygame.font.SysFont("Times New Roman", 80)
box_font = pygame.font.SysFont("Times New Roman", 30)

title_text = title_font.render("Tetris", True, white)
start_text = menu_font.render("Press Enter to Start", True, white)
start_text = pygame.transform.rotate(start_text, 270)
pause_text = menu_font.render("Pause", True, white)
pause_text = pygame.transform.rotate(pause_text, 270)
game_over_text = menu_font.render("Game Over", True, white)
game_over_text = pygame.transform.rotate(game_over_text, 270)
next_text = box_font.render("Next", True, white)
hold_text = box_font.render("Hold", True, white)
level_text = box_font.render("Level", True, white)
level_text2 = box_font.render(str(level), True, white)
score_text = box_font.render("Score", True, white)
score_text2 = box_font.render(str(score), True, white)
name_text = box_font.render("Made by Paulo Bello", True, white)
version_text = box_font.render("v1.0", True, white)

grid = []
for x in range(20):
    row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    grid.append(row)


class Block:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def draw(self):
        pygame.draw.rect(window, self.color, (100 + self.position[0] * 30, 100 + self.position[1] * 30, 30, 30))


class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.block_list = []
        self.piece_frame = 0
        self.active = False

        match self.shape:
            case "i":
                self.block_list = [Block(light_blue, [11.5, 2]), Block(light_blue, [12.5, 2]),
                                   Block(light_blue, [13.5, 2]),
                                   Block(light_blue, [14.5, 2])]
            case "j":
                self.block_list = [Block(blue, [12, 1.5]), Block(blue, [12, 2.5]), Block(blue, [13, 2.5]),
                                   Block(blue, [14, 2.5])]
            case "l":
                self.block_list = [Block(orange, [12, 2.5]), Block(orange, [13, 2.5]), Block(orange, [14, 2.5]),
                                   Block(orange, [14, 1.5])]
            case "o":
                self.block_list = [Block(yellow, [12.5, 1.5]), Block(yellow, [12.5, 2.5]), Block(yellow, [13.5, 1.5]),
                                   Block(yellow, [13.5, 2.5])]
            case "s":
                self.block_list = [Block(green, [12, 2.5]), Block(green, [13, 2.5]), Block(green, [13, 1.5]),
                                   Block(green, [14, 1.5])]
            case "t":
                self.block_list = [Block(purple, [12, 2.5]), Block(purple, [13, 2.5]), Block(purple, [14, 2.5]),
                                   Block(purple, [13, 1.5])]
            case "z":
                self.block_list = [Block(red, [12, 1.5]), Block(red, [13, 1.5]), Block(red, [13, 2.5]),
                                   Block(red, [14, 2.5])]

        for block in self.block_list:
            pygame.draw.rect(window, block.color, (100 + block.position[0] * 30, 100 + block.position[1] * 30, 30, 30))

    def move(self, direction="down"):
        global switch_ready
        global bottom_frame

        if direction == "left":
            for block in self.block_list:
                if block.position[0] <= 0:
                    return
                if block.position[0] > 0 and grid[block.position[1]][block.position[0] - 1] == 1:
                    return
            for block in self.block_list:
                block.position[0] -= 1

        elif direction == "right":
            for block in self.block_list:
                if block.position[0] >= 9:
                    return
                if grid[block.position[1]][block.position[0] + 1] == 1:
                    return
            for block in self.block_list:
                block.position[0] += 1

        elif direction == "down":
            for block in self.block_list:
                if switch_ready is not True and (
                        (block.position[1] < 19 and grid[block.position[1] + 1][block.position[0]] == 1) or
                        block.position[1] == 19):
                    switch_ready = True
                    bottom_frame = self.piece_frame
                    return False
                elif switch_ready and (
                        (block.position[1] < 19 and grid[block.position[1] + 1][block.position[0]] == 1) or
                        block.position[1] == 19):
                    return False
            for block in self.block_list:
                block.position[1] += 1

    def rotate(self):
        if self.shape == "o":
            return

        pivot = self.block_list[1]
        new_block_list = []

        for block in self.block_list:

            relative_x = block.position[0] - pivot.position[0]
            relative_y = block.position[1] - pivot.position[1]

            temp = -relative_x
            relative_x = relative_y
            relative_y = temp

            new_x = pivot.position[0] + relative_x
            new_y = pivot.position[1] + relative_y

            if new_x < 0 or new_x > 9 or new_y < 0 or new_y > 19 or grid[new_y][new_x] == 1:
                return

            new_block = Block(block.color, [new_x, new_y])
            new_block_list.append(new_block)

        self.block_list = new_block_list

    def draw(self):
        if self.active:
            for block in self.block_list:
                block.draw()
            self.piece_frame += 1
        else:
            for block in self.block_list:
                block.draw()

    def activate(self):
        match self.shape:
            case "i":
                self.block_list = [Block(light_blue, [3, 0]), Block(light_blue, [4, 0]), Block(light_blue, [5, 0]),
                                   Block(light_blue, [6, 0])]
            case "j":
                self.block_list = [Block(blue, [3, 0]), Block(blue, [3, 1]), Block(blue, [4, 1]),
                                   Block(blue, [5, 1])]
            case "l":
                self.block_list = [Block(orange, [3, 1]), Block(orange, [4, 1]), Block(orange, [5, 1]),
                                   Block(orange, [5, 0])]
            case "o":
                self.block_list = [Block(yellow, [4, 0]), Block(yellow, [4, 1]), Block(yellow, [5, 0]),
                                   Block(yellow, [5, 1])]
            case "s":
                self.block_list = [Block(green, [3, 1]), Block(green, [4, 1]), Block(green, [4, 0]),
                                   Block(green, [5, 0])]
            case "t":
                self.block_list = [Block(purple, [3, 1]), Block(purple, [4, 1]), Block(purple, [5, 1]),
                                   Block(purple, [4, 0])]
            case "z":
                self.block_list = [Block(red, [3, 0]), Block(red, [4, 0]), Block(red, [4, 1]), Block(red, [5, 1])]
        self.active = True

    def hold(self):
        global piece_held
        match self.shape:
            case "i":
                self.block_list = [Block(light_blue, [11.5, 9]), Block(light_blue, [12.5, 9]),
                                   Block(light_blue, [13.5, 9]),
                                   Block(light_blue, [14.5, 9])]
            case "j":
                self.block_list = [Block(blue, [12, 8.5]), Block(blue, [12, 9.5]), Block(blue, [13, 9.5]),
                                   Block(blue, [14, 9.5])]
            case "l":
                self.block_list = [Block(orange, [12, 9.5]), Block(orange, [13, 9.5]), Block(orange, [14, 9.5]),
                                   Block(orange, [14, 8.5])]
            case "o":
                self.block_list = [Block(yellow, [12.5, 8.5]), Block(yellow, [12.5, 9.5]), Block(yellow, [13.5, 8.5]),
                                   Block(yellow, [13.5, 9.5])]
            case "s":
                self.block_list = [Block(green, [12, 9.5]), Block(green, [13, 9.5]), Block(green, [13, 8.5]),
                                   Block(green, [14, 8.5])]
            case "t":
                self.block_list = [Block(purple, [12, 9.5]), Block(purple, [13, 9.5]), Block(purple, [14, 9.5]),
                                   Block(purple, [13, 8.5])]
            case "z":
                self.block_list = [Block(red, [12, 8.5]), Block(red, [13, 8.5]), Block(red, [13, 9.5]),
                                   Block(red, [14, 9.5])]
        self.active = False


current_piece = Piece(piece_list[random.randint(0, 6)])
current_piece.activate()
next_piece = Piece(piece_list[random.randint(0, 6)])
past_blocks = []


def piece_switch(held=False):
    global current_piece
    global switch_ready
    global next_piece
    global past_blocks
    global piece_held
    global held_piece
    global recent_piece_hold
    global game_over

    if not held:
        for block in current_piece.block_list.copy():
            past_blocks.append(block)
            current_piece.block_list.remove(block)
        current_piece = next_piece
        current_piece.activate()
        next_piece = Piece(piece_list[random.randint(0, 6)])
        switch_ready = False
        recent_piece_hold = False

    else:
        if piece_held:
            recent_piece_hold = True
            temp = held_piece
            held_piece = current_piece
            held_piece.hold()
            current_piece = temp
            current_piece.activate()
        else:
            piece_held = True
            recent_piece_hold = True
            held_piece = current_piece
            held_piece.hold()
            current_piece = next_piece
            current_piece.activate()
            next_piece = Piece(piece_list[random.randint(0, 6)])


def update_score(type, lines_cleared=0, blocks_dropped=0):
    global score
    global level
    global total_lines
    global score_text2

    if type == "line_clear":
        total_lines += lines_cleared
        match lines_cleared:
            case 1:
                score += 40 * (level + 1)
            case 2:
                score += 100 * (level + 1)
            case 3:
                score += 300 * (level + 1)
            case 4:
                score += 1200 * (level + 1)
    elif type == "soft_drop":
        score += 1
    elif type == "hard_drop":
        score += 2 * blocks_dropped

    score_text2 = box_font.render(str(score), True, white)


def hard_drop():
    global current_piece
    global grid

    # finds the lowest possible blocks to reach a surface
    square_count_list = []
    for block in current_piece.block_list:
        counter = 0
        while block.position[1] + counter < 19 and grid[block.position[1] + counter][block.position[0]] == 0:
            counter += 1
        square_count_list.append(counter)
    square_count = min(square_count_list)

    for block in current_piece.block_list:
        if grid[block.position[1] + square_count][block.position[0]] == 1:
            square_count -= 1

    for block in current_piece.block_list:
        block.position[1] += square_count

    update_score("hard_drop", blocks_dropped=square_count)
    piece_switch()


def remove_blocks(past_blocks, row):
    copy_blocks = []
    for block in past_blocks:
        if block.position[1] != row:
            copy_blocks.append(block)

    return copy_blocks


def line_clear_check():
    global grid
    global past_blocks

    lines_filled = 0
    for y in range(19, 0, -1):
        squares_filled = 0

        for x in range(10):
            if grid[y][x] == 1:
                squares_filled += 1

        if squares_filled == 10:
            lines_filled += 1
            past_blocks = remove_blocks(past_blocks, y)
            for block in past_blocks:
                if (block.position[1] < y):
                    block.position[1] += 1
            break

    update_score("line_clear", lines_cleared=lines_filled)


def level_up():
    global level
    global speed
    global required_lines
    global total_lines
    global level_text2

    level += 1
    level_text2 = box_font.render(str(level), True, white)

    if level <= 8:
        speed -= 5
    elif level == 9:
        speed = 6
    elif level == 10:
        speed = 5
    elif level == 13:
        speed = 4
    elif level == 16:
        speed = 3
    elif level == 19:
        speed = 2
    elif level == 29:
        speed = 1

    if level <= 9:
        required_lines = 10 * (level + 1)
    if 16 <= level <= 25:
        required_lines = 10 * (level - 5)

    total_lines = 0
    print("Level up!")  # for testing, remove later


# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and menu:
            if event.key == pygame.K_RETURN:
                menu = False
        if event.type == pygame.KEYDOWN and not menu:
            if event.key == pygame.K_ESCAPE:
                pause_menu = not pause_menu

        if event.type == pygame.KEYDOWN and not menu and not pause_menu and not game_over:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                current_piece.move("left")
                if switch_ready:
                    bottom_frame = current_piece.piece_frame
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                current_piece.move("right")
                if switch_ready:
                    bottom_frame = current_piece.piece_frame
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                current_piece.rotate()
                if switch_ready:
                    bottom_frame = current_piece.piece_frame
            elif event.key == pygame.K_c and not recent_piece_hold:
                piece_switch(held=True)
            elif event.key == pygame.K_SPACE:
                hard_drop()

    # active loop
    if not menu and not pause_menu and not game_over:
        for block in current_piece.block_list:
            if ((block.position[1] < 19 and grid[block.position[1] + 1][block.position[0]] == 1) or block.position[1] == 19):
                touching_bottom = True

        if (pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]) and speed != 1 and not touching_bottom:
            fast_drop = True

        if fast_drop:
            if current_piece.piece_frame % (speed / 2) == 0 and current_piece.piece_frame != 0:
                current_piece.move()
                update_score("soft_drop")
        else:
            if current_piece.piece_frame % speed == 0 and current_piece.piece_frame != 0:
                current_piece.move()

        for block in current_piece.block_list:
            if switch_ready and not touching_bottom:
                switch_ready = False

        if switch_ready and current_piece.piece_frame >= bottom_frame + speed and touching_bottom:
            piece_switch()

        for x in range(len(grid)):
            for y in range(len(grid[x])):
                grid[x][y] = 0

        for block in past_blocks:
            grid[block.position[1]][block.position[0]] = 1

        for i in range(10):
            if grid[0][i] == 1:
                game_over = True
                break


        line_clear_check()

        if total_lines - required_lines == 0:
            level_up()

    window.fill((0, 0, 0))

    window.blit(title_text, (100, 20))

    for x in range(20):
        pygame.draw.line(window, gray, (98, 100 + 30 * x), (400, 100 + 30 * x))
    for x in range(10):
        pygame.draw.line(window, gray, (100 + 30 * x, 98), (100 + 30 * x, 700))
    pygame.draw.rect(window, white, (98, 98, 304, 604), 2)

    window.blit(name_text, (10, 760))
    window.blit(version_text, (640, 760))

    if menu:
        window.blit(start_text, (500, 60))

    elif pause_menu:
        window.blit(pause_text, (500, 60))

        if past_blocks:
            for block in past_blocks:
                block.draw()

    elif game_over:
        window.blit(game_over_text, (500, 60))

        if past_blocks:
            for block in past_blocks:
                block.draw()

    else:
        pygame.draw.rect(window, white, (430, 98, 150, 150), 2)
        pygame.draw.rect(window, white, (430, 308, 150, 150), 2)
        window.blit(next_text, (430, 68))
        window.blit(hold_text, (430, 278))
        window.blit(level_text, (430, 488))
        window.blit(level_text2, (430, 518))
        window.blit(score_text, (430, 578))
        window.blit(score_text2, (430, 608))

        current_piece.draw()
        next_piece.draw()
        if piece_held:
            held_piece.draw()

        if past_blocks:
            for block in past_blocks:
                block.draw()

    fast_drop = False
    touching_bottom = False

    pygame.display.update()
    clock.tick(60)
