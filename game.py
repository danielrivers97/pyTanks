import pygame
from network import Network


class Player():
    width = height = 20

    def __init__(self, startX, startY, color=(255,0,0)):
        self.x = startX 
        self.y = startY 
        self.mouse_pos = (0, 0)
        self.velocity = 1
        self.color = color
        self.bullet = (-1, -1)
        self.bulletDirrection = (0, 0)
        self.bulletSpeed = 5

    def draw(self, g):
        mx = int(self.x + (self.width / 2))
        my = int(self.y + (self.height / 2))
        dx = self.mouse_pos[0] - mx
        dy = self.mouse_pos[1] - my
        h = (dx**2 + dy**2)**0.5
        armL = 15.0
        ratio = armL / h
        nx = mx + dx * ratio
        ny = my + dy * ratio

        # draw tank
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)
        pygame.draw.line(g, (255,50,50), (mx, my), (nx, ny), 8)
        pygame.draw.circle(g, (255,100,100), (mx, my), 7)

        # draw bullet
        pygame.draw.circle(g, (100,100,100), (int(self.bullet[0]), int(self.bullet[1])), 3)

        # calculate next bulet location
        bullet = (self.bullet[0] + self.bulletDirrection[0], 
                  self.bullet[1] + self.bulletDirrection[1])
        self.bullet = bullet


    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def fire(self):
        mx = int(self.x + (self.width / 2))
        my = int(self.y + (self.height / 2))
        dx = self.mouse_pos[0] - mx
        dy = self.mouse_pos[1] - my
        h = (dx**2 + dy**2)**0.5
        armL = 15.0
        ratio = self.bulletSpeed / h
        nx = dx * ratio
        ny = dy * ratio
        self.bullet = (mx, my)
        self.bulletDirrection = (nx, ny)


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.screen_size = [w, h]
        self.player = Player(50, 50)
        self.player2 = Player(100,100)
        self.canvas = Canvas(self.width, self.height, "Testing...")

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Tanks")
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            self.player.mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.player.fire()

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if self.player.x + self.player.width + self.player.velocity <= self.width:
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y + self.player.height + self.player.velocity <= self.height:
                    self.player.move(3)

            # Send Network Stuff
            self.parse_data(self.send_data())

            # Update Screen
            screen.fill((200,220,245))
            self.player.draw(screen)
            self.player2.draw(screen)
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        mx = str(self.player.mouse_pos[0])
        my = str(self.player.mouse_pos[1])
        bx = str(self.player.bullet[0])
        by = str(self.player.bullet[1])
        dx = str(self.player.bulletDirrection[0])
        dy = str(self.player.bulletDirrection[1])
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y) + "," + mx + "," + my + "," + bx + "," + by + "," + dx + "," + dy
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            # Player:    x          y    mouse x    mouse y   bullet x   bullet y  bullet dx  bullet dy
            self.player2.x = int(d[0])
            self.player2.y = int(d[1])
            self.player2.mouse_pos = (int(d[2]), int(d[3]))
            self.player2.bullet = (int(d[4]), int(d[5]))
            self.player2.bulletDirrection = (float(d[6]), float(d[7]))
            return 0
        except:
            return -1


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))
