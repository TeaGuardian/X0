from socket import *
import pygame


def get_ip():
    h_name = gethostname()
    return gethostbyname(h_name)


class Server:
    def __init__(self, port=12000, buffer=1024):
        """порт соединения и размер буфера"""
        self.s_port, self.buf = port, buffer
        self.con = None

    def wait_client(self):
        """создаёт соединение и возвращает адрес"""
        if self.con is not None:
            print('connection is already there')
            return None
        server = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind(('', self.s_port))
        server.listen(1)
        print("waiting for client connecting...")
        self.con, addr = server.accept()
        self.con.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        print(self.con.getsockopt(SOL_SOCKET, SO_KEEPALIVE))
        print('SUCCESS')
        server.close()
        return addr

    def close_c(self):
        """закрывает соединение"""
        self.con.shutdown(SHUT_RDWR)
        self.con.close()
        print('CLOSED')
        return None

    def communicate(self, text=''):
        """шлёт и принимает данные, если передан не текст - кладёт трубку"""
        try:
            self.con.send(text.encode())
        except ConnectionResetError as e:
            print("Server connection closed")
            return "ERROR"
        try:
            sentence = self.con.recv(self.buf).decode()
        except ConnectionResetError as e:
            print("Client connection closed")
            return "ERROR"
        if len(sentence) == 0:
            return "ERROR"
        return sentence


class Client:
    def __init__(self, ip='192.168.43.1', port=12000, buffer=1024):
        """ip сервера, порт соединения и размер буфера"""
        self.s_port, self.buf, self.ip = port, buffer, ip
        self.con = None

    def wait_server(self):
        """создаёт соединение и возвращает адрес"""
        if self.con is not None:
            print('connection is already there')
            return None
        self.con = socket(AF_INET, SOCK_STREAM)
        try:
            self.con.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
            self.con.connect((self.ip, self.s_port))
            print(self.con.getsockopt(SOL_SOCKET, SO_KEEPALIVE))
        except ConnectionRefusedError as e:
            self.con = None
            print('server refused but exists')
            return None
        return self.ip

    def close_c(self):
        """закрывает соединение"""
        self.con.shutdown(SHUT_RDWR)
        self.con.close()
        print('CLOSED')
        return None

    def communicate(self, text=''):
        """принимает данные и шлёт, если передан не текст - кладёт трубку"""
        try:
            sentence = self.con.recv(self.buf).decode()
        except ConnectionResetError as e:
            print("Client connection closed")
            return "ERROR"
        if len(sentence) == 0:
            return "ERROR"
        try:
            self.con.send(text.encode())
        except ConnectionResetError as e:
            print("Server connection closed")
            return "ERROR"
        return sentence


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
        self.last = self.to_send[:]
        self.font = pygame.font.Font(None, 50)
        self.p, self.tern = p, '0'
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
            if event.type == pygame.MOUSEBUTTONDOWN and self.p == self.tern:
                for x in range(3):
                    for y in range(3):
                        if self.field[x][y].get()[1] == self.colors[0] and alz[x][y]:
                            self.field[x][y].rename(self.var[int(self.p)], self.colors[int(self.p) + 1])
                            self.to_send[0], self.to_send[1] = str(x), str(y)
                            if self.tern == '0':
                                self.tern = '1'
                            else:
                                self.tern = '0'
                            self.to_send[2] = str(int(self.p) + 1)
                            self.to_send[3] = self.tern
        answer = self.con.communicate('#'.join(self.to_send)).split('#')
        if answer is None or len(answer) < 3:
            return 'ERROR'
        if 'n' in answer:
            return 0
        if answer != self.last:
            self.last = answer[:]
            if self.tern == '0':
                self.tern = '1'
            else:
                self.tern = '0'
            pv, pu = int(answer[0]), int(answer[1])
            self.field[pv][pu].rename(self.var[int(answer[2]) - 1], self.colors[int(answer[2])])
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
    font = pygame.font.Font(None, 50)
    b1 = Button(50, 50, 1200, 100, 'CREATE SERVER', [200, 200, 200], screen)
    b2 = Button(50, 300, 1200, 100, 'CREATE CLIENT', [200, 200, 200], screen)
    pf = 1
    while pf:
        screen.fill([50, 50, 50])
        rb1, rb2 = b1.show(), b2.show()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rb1:
                    con = Server()
                    stext = font.render("WAITING FOR CLIENT", True, [255, 255, 255])
                    screen.blit(stext, (200, 100))
                    pygame.display.update()
                    print(con.wait_client())
                    r ='0'
                    pf = 0
                elif rb2:
                    con = Client('192.168.43.1')
                    stext = font.render("WAITING FOR SERVER", True, [255, 255, 255])
                    screen.blit(stext, (200, 100))
                    pygame.display.update()
                    while con.wait_server() is None:
                        pass
                    r = '1'
                    pf = 0
        pygame.display.update()
    field = Field(con, screen, r)
    while True:
        screen.fill([50, 50, 50])
        field.update()
        pygame.display.update()


main()