#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame
import math

from draw_utils import colors, rink

def addVectors(angle1, length1, angle2, length2):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    angle  = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)
    return (angle, length)

def collide(p1, p2):    
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist = math.hypot(dx, dy)
    if dist < p1.radius + p2.radius:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass, angle, 2*p2.speed*p2.mass/total_mass)
        (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass, angle+math.pi, 2*p1.speed*p1.mass/total_mass)
        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5*(p1.radius + p2.radius - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap
        

class MovingObject(object):
    def __init__(self, radius, mass=1):
        self.radius = radius
        self.limit = {}
        self.limit['left'],  self.limit['top']    = rink['left']+radius,  rink['top']+radius
        self.limit['right'], self.limit['bottom'] = rink['right']-radius, rink['bottom']-radius
        
        self.x, self.y = self.start_x, self.start_y = 0, 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.9
        
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.speed = 0
        self.angle = 0
 
class Puck(MovingObject):
    def __init__(self, radius=15):
        super().__init__(radius)
        self.x, self.y = self.start_x, self.start_y = rink['center_x'], rink['center_y']
        
    def update(self):
        def move():          
            self.x += math.sin(self.angle) * self.speed
            self.y -= math.cos(self.angle) * self.speed
            self.speed *= self.drag
            
        def bounce():
            if self.x > self.limit['right']:
                self.x = self.limit['right']
                self.angle = -self.angle
                self.speed *= self.elasticity
            elif self.x < self.limit['left']:
                self.x = self.limit['left']
                self.angle = -self.angle
                self.speed *= self.elasticity
        
            if self.y > self.limit['bottom']:
                self.y = self.limit['bottom']
                self.angle = math.pi - self.angle
                self.speed *= self.elasticity
            elif self.y < self.limit['top']:
                self.y = self.limit['top']
                self.angle = math.pi - self.angle
                self.speed *= self.elasticity
        move()
        bounce()
            
    def draw(self, screen):
        pygame.draw.circle(screen, colors['black'], [int(self.x), int(self.y)], 15, 0)


class Mallet(MovingObject):
    def __init__(self, radius=20, mass=15):
        super().__init__(radius, mass)
            
    def update(self):            
        if self.x   <=  self.limit['left']:
            self.x  =   self.limit['left']
        elif self.x >=  self.limit['right']:
            self.x  =   self.limit['right']
            
        if self.y   <=  self.limit['top']:
            self.y  =   self.limit['top']
        elif self.y >=  self.limit['bottom']:
            self.y  =   self.limit['bottom']
        
    def draw(self, screen):
        pygame.draw.circle(screen, colors['red'], [int(self.x), int(self.y)], 20, 0)
        pygame.draw.circle(screen, colors['black'], [int(self.x), int(self.y)], 20, 1)
        pygame.draw.circle(screen, colors['black'], [int(self.x), int(self.y)], 5,  0)
        
class PlayerMallet(Mallet):
    def __init__(self, radius=20,):
        super().__init__(radius)
        self.x, self.y = self.start_x, self.start_y = rink['center_x'], rink['bottom']-radius
        self.limit['top'] = rink['center_y'] + self.radius
            
    def update(self, mouseX=0, mouseY=0):
        dx = mouseX - self.x
        dy = mouseY - self.y
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy)
        
        self.x, self.y = mouseX, mouseY
        
        super().update()
        
class CpuMallet(Mallet):
    def __init__(self, radius=20):
        super().__init__(radius)
        self.x, self.y = self.start_x, self.start_y = rink['center_x'], rink['top']+radius
        self.limit['bottom'] = rink['center_y'] - self.radius
    
    def update(self, puck):
        dx = 0
        dy = 0
        if puck.x < self.x:
            if puck.x < self.limit['left']:
                dx = 1
            else:
                dx = -2
        if puck.x > self.x:
            if  puck.x > self.limit['right']:
                dx = -1
            else:
                dx = 2
        if puck.y < self.y:
            if puck.y < self.limit['top']:
                dy = 1
            else:
                dy = -6
        if puck.y > self.y:
            if puck.y <= 360:
                dy = 6
            else:
                if self.y > 200:
                    dy = -2
                else:
                    dy = 0
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy)
        
        self.x, self.y = self.x + dx, self.y + dy
        super().update()

class Goal(object):
    def __init__(self,x,y,w=100,h=20):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.centre_x = self.x + self.w/2
        self.centre_y = self.y + self.w/2
                
    def draw(self, screen):
        pygame.draw.rect(screen, colors['green'], (self.x,self.y,self.w,self.h), 0)
        

class Environment:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.elasticity = 0.75
        
        self.puck = Puck()
        self.playerMallet = PlayerMallet()
        self.cpuMallet = CpuMallet()
        
        self.cpuGoal    = Goal(200, 15)
        self.playerGoal = Goal(200, 660)
        
    def update(self, mouseX, mouseY):        
        
        self.puck.update()
        
        self.playerMallet.update(mouseX, mouseY)
        self.cpuMallet.update(self.puck)
        
        collide(self.puck, self.playerMallet)
        collide(self.puck, self.cpuMallet)
        
        if (abs(self.playerGoal.centre_y-self.puck.y) <= 50 and abs(self.playerGoal.centre_x-self.puck.x) <= 50):
            print("Computer Scores!")
            self.puck.reset()
            self.cpuMallet.reset()
    
        if (abs(self.cpuGoal.centre_y-self.puck.y) <= 50 and abs(self.cpuGoal.centre_x-self.puck.x) <= 50):
            print("Player Scores!")
            self.puck.reset()
            self.cpuMallet.reset()
        
    def get_drawables(self):
        return [self.puck, self.playerMallet, self.cpuMallet, self.cpuGoal, self.playerGoal]
    