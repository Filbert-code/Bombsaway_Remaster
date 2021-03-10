import pygame
import constants

def draw_text(surf, text, size, x, y, color, font_name):
    font_name = pygame.font.match_font(font_name)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
