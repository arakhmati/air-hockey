#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame

colors = {
     'black': (   0,   0,   0),
     'white': ( 255, 255, 255),
     'green': (   0, 255,   0),
     'red':   ( 255,   0,   0),
     'blue':  (   0,   0, 255),
}

width, height = (500, 700)
margin = 25

rink = {}
rink['margin'] = margin
rink['left'],     rink['top']      = rink['margin'], rink['margin']
rink['right'],    rink['bottom']   = width-rink['margin'], height-rink['margin']
rink['width'],    rink['height']   = rink['right']-rink['left'], rink['bottom']-rink['top']
rink['center_x'], rink['center_y'] = width//2, height//2

def draw_rink(screen):
    pygame.draw.rect(screen, colors['white'], (rink['left'], rink['top'], rink['width'], rink['height']), 0)
    
    #middle section
    pygame.draw.line(screen, colors['red'], [rink['left'], rink['center_y']], [rink['right'], rink['center_y']], 5)
    pygame.draw.circle(screen, colors['red'], [rink['center_x'], rink['center_y']], 50, 5)
    pygame.draw.circle(screen, colors['red'], [rink['center_x'], rink['center_y']], 10)
    
#    #end of middle section
#    pygame.draw.line(screen, colors['blue'], [rink['left'], 250], [rink['right'], 250],5)
#    pygame.draw.line(screen, colors['blue'], [rink['left'], 450], [rink['right'], 450],5)
    
    #decorative circles
#    for x in range(125,376,250):
#        for y in range(175,526,350):
#            pygame.draw.circle(screen, colors['red'], [x,y],50,5)
#            pygame.draw.circle(screen, colors['red'], [x,y],10)
    #end lines        
#    pygame.draw.line(screen, colors['red'], [25,50],[475,50],2)
#    pygame.draw.line(screen, colors['red'], [25,650],[475,650],2)
    
    #rink frame   
    pygame.draw.rect(screen, colors['black'], (rink['left'], rink['top'], rink['width'], rink['height']), 5)