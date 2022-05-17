import pygame


class Button:
    def __init__(self, x, y, hx, hy, text, color, screen):
        self.x, self.y, self.hx, self.hy = x, y, hx, hy
        self.name, self.col, self.nc = text, color, color
        self.screen = screen
        self.font = pygame.font.Font(None, 50)

    def show(self):
        px, py = pygame.mouse.get_pos()
        flag = px in range(self.x, self.x + self.hx) and py in range(self.y, self.y + self.hy)
        if flag:
            self.col = list(map(lambda dx: dx * 50 // 100, self.nc[:]))
        else:
            self.col = self.nc[:]
        r = self.hy // 10
        pygame.draw.rect(self.screen, self.col, ((self.x - r, self.y), (self.hx + r * 2, self.hy)))
        pygame.draw.rect(self.screen, self.col, ((self.x, self.y - r), (self.hx, self.hy + r * 2)))
        pygame.draw.circle(self.screen, self.col, (self.x, self.y), r)
        pygame.draw.circle(self.screen, self.col, (self.x + self.hx, self.y), r)
        pygame.draw.circle(self.screen, self.col, (self.x, self.y + self.hy), r)
        pygame.draw.circle(self.screen, self.col, (self.x + self.hx, self.y + self.hy), r)
        if self.name != '':
            b_text = self.font.render(self.name, True, [255 - self.col[0], 255 - self.col[1], 255 - self.col[2]])
            self.screen.blit(b_text, (self.x + self.hx * 0.65 - len(self.name) * 30, self.y + self.hy * 0.3))
        return flag

    def rename(self, text, color):
        self.name = text
        self.nc = color

    def get(self):
        return [self.name, self.nc]


class Field:
    def __init__(self, con, screen, p):
        self.to_send = ['n', 'n', '0', '0']
        self.var = ['0', 'X']
        self.font = pygame.font.Font(None, 50)
        self.tern = '0'
        self.colors = [[150, 150, 150], [150, 20, 20], [20, 20, 150]]
        self.con, self.screen = con, screen
        self.cx, self.cy = self.screen.get_size()
        self.field = [[0 for i in range(3)] for _ in range(3)]
        if self.cx > self.cy:
            self.cx = self.cx // 2
        else:
            self.cx = (self.cx * 85) // 100
            self.cy = (self.cy * 85) // 100
        self.hx, self.hy = (self.cx * 24) // 100, (self.cy * 24) // 100
        for x in range(3):
            for y in range(3):
                lx = int((x + 1) * self.cy * 0.06 + x * self.hx)
                ly = int((y + 1) * self.cy * 0.06 + y * self.hy)
                self.field[x][y] = Button(lx, ly, self.hx, self.hy, '', self.colors[0], screen)

    def get_winer(self):
        d = [[0 for i in range(3)] for _ in range(3)]
        red, blue = self.var
        for x in range(3):
            for y in range(3):
                d[x][y] = self.field[x][y].get()[0]

        for y in range(3):
            if d[0][y] == d[1][y] == d[2][y]:
                if d[0][y] == blue:
                    return 'Победили синие'
                elif d[0][y] == red:
                    return 'Победили красные'
            elif d[y][0] == d[y][1] == d[y][2]:
                if d[y][0] == blue:
                    return 'Победили синие'
                elif d[y][0] == red:
                    return 'Победили красные'
        if d[0][0] == d[1][1] == d[2][2]:
            if d[0][0] == blue:
                return 'Победили синие'
            elif d[0][0] == red:
                return 'Победили красные'
        if d[2][0] == d[1][1] == d[0][2]:
            if d[1][1] == blue:
                return 'Победили синие'
            elif d[1][1] == red:
                return 'Победили красные'
        for x in range(3):
            for y in range(3):
                if d[x][y] not in self.var:
                    return 'игра продолжается'
        return 'НИЧЬЯ'


    def update(self):
        alz = [[0 for i in range(3)] for _ in range(3)]
        for x in range(3):
            for y in range(3):
                alz[x][y] = self.field[x][y].show()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(3):
                    for y in range(3):
                        if self.field[x][y].get()[1] == self.colors[0] and alz[x][y]:
                            self.field[x][y].rename(self.var[int(self.tern)], self.colors[int(self.tern) + 1])
                            if self.tern == '0':
                                self.tern = '1'
                            else:
                                self.tern = '0'
        ext = self.get_winer()
        text = self.font.render(ext, True, [255, 215, 0])
        self.screen.blit(text, (25, 25))
        return 0


"""
field = Field(0, screen, '1')
    while True:
        field.update()
        pygame.display.update()
"""




def main():
    pygame.init()
    r, con = 0, 0
    screen = pygame.display.set_mode()
    field = Field(con, screen, r)
    while True:
        screen.fill([50, 50, 50])
        field.update()
        pygame.display.update()


main()