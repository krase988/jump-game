class Character:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (0, 0, 255)  # Blue color

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)