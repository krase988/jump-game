def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def random_position(width, height):
    import random
    return random.randint(0, width), random.randint(0, height)