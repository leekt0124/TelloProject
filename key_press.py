import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))

def get_key(key_name):
    ans = False
    for event in pygame.event.get():
        pass
    key_input = pygame.key.get_pressed()
    my_key = getattr(pygame, 'K_{}'.format(key_name))
    if key_input[my_key]:
        ans = True
    pygame.display.update()
    return ans

def main():
    print(get_key("a"))

if __name__ == '__main__':
    init()
    while True:
        main()