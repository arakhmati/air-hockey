import pygame
import random
from abc import ABC, abstractmethod

from Vector import Vector
from MovingCircle import MovingCircle
from physics_utils import angle_from_O, distance_from_O, angle, distance
from color_utils import colors

import numpy as np

#class MalletFactory:
#    def


class Mallet(MovingCircle, ABC):
    def __init__( self, player, rink, puck, color=colors['red'], radius=20, mass=20, max_speed=0.6, friction=0.0001, acceleration=0.0025):
        
        self.__player = player
        if self.get_player() == 'top':
            pos = (rink.get_center_x(), rink.get_top()    + rink.get_margin())
        elif self.get_player() == 'bottom':
            pos = (rink.get_center_x(), rink.get_bottom() - rink.get_margin())
        else:
            raise ValueError("player can be either 'top' or 'bottom'")
            
        super().__init__(pos, rink, radius, mass, max_speed, friction)
        
        self.__acceleration = acceleration
        self.__puck = puck
        self.__color = color
        
        if self.get_player() == 'top':
            self.__top_bound    = self.get_rink().get_top() + self.get_radius()
            self.__bottom_bound = self.get_rink().get_top() + 0.5*(self.get_rink().get_height()) - self.get_radius()
        elif self.get_player() == 'bottom':
            self.__top_bound    = self.get_rink().get_top() + 0.5*(self.get_rink().get_height()) + self.get_radius()
            self.__bottom_bound = self.get_rink().get_top() + self.get_rink().get_height() - self.get_radius()
        
    def get_acceleration(self):
        return self.__acceleration

    def get_player(self):
        return self.__player
    
    def get_puck(self):
        return self.__puck
    
    def get_top_bound(self):
        return self.__top_bound
    
    def get_bottom_bound(self):
        return self.__bottom_bound
            
    def set_acceleration(self,acceleration):
        self.__acceleration = acceleration

    def set_player(self,player):
        self.__player = player
        
    def draw( self, screen):
        x, y = self.get_pos().get_xy()
        pygame.draw.circle(screen, self.__color,   [int(x), int(y)], self.get_radius(), 0)
        pygame.draw.circle(screen, colors['black'], [int(x), int(y)], self.get_radius(), 1)
        pygame.draw.circle(screen, colors['black'], [int(x), int(y)], 5,  0)
    
    @abstractmethod
    def move(self, dt):
        pass
    
    def overlaps(self):
        R0 = self.get_radius()
        R1 = self.get_puck().get_radius()
        x0, y0 = self.get_pos_xy()
        x1, y1 = self.get_puck().get_pos_xy()
        return (R0-R1)**2 <= (x0-x1)**2+(y0-y1)**2 <= (R0+R1)**2
        
class KeyboardMallet(Mallet):
    
    def move(self, dt):
        
        touched = False
        self.friction(dt)
        old_px, old_py = self.get_pos_xy()
        puck_px, puck_py = self.get_puck().get_pos_xy()
        
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_a]: x = -1  
        elif keys[pygame.K_d]: x = 1
        else: x = 0.0                  
        if keys[pygame.K_w]: y = -1       
        elif keys[pygame.K_s]: y = 1     
        else: y = 0.0
        
#        if p == 2:
#            keys = pygame.key.get_pressed()  
#            if keys[pygame.K_LEFT]: x = -1.0    
#            elif keys[pygame.K_RIGHT]: x = 1.0  
#            else: x = 0.0                  
#            if keys[pygame.K_UP]: y = -1.0          
#            elif keys[pygame.K_DOWN]: y = 1.0       
#            else: y = 0.0
 
        vx,vy = self.get_speed_xy()
        vx += x*self.get_acceleration()*dt
        vy += y*self.get_acceleration()*dt
        
        self.set_speed_angle(angle_from_O((vx,vy)))
        new_speed = distance_from_O((vx,vy))
        if new_speed<=self.get_max_speed():
            self.set_speed_magnitude (new_speed)
 
        new_pos = self.get_pos()+dt*self.get_speed()
        px,py = new_pos.get_xy()
        
        if (px < self.get_rink().get_left()+self.get_radius()):
            px = self.get_rink().get_left()+self.get_radius()
            touched = True
        elif (px > self.get_rink().get_right()-self.get_radius()):
            px = self.get_rink().get_right()-self.get_radius()
            touched = True
        
        if (py < self.get_top_bound()):
            py = self.get_top_bound()
            touched = True
        elif (py > self.get_bottom_bound()):
            py = self.get_bottom_bound()
            touched = True
            
        # Prevent from oscillating near the borders
        if touched:
            old_pos = self.get_pos_xy()
            self.set_speed_angle(angle(old_pos,(px,py)))
            self.set_speed_magnitude(distance(old_pos,(px,py))/dt)
            
        
        if self.overlaps():
            x = (old_px - puck_px) > 0
            px = old_px + x * 5
            y = (old_py - puck_py) > 0
            py = old_py + y * 5
        
        self.set_pos_xy((px, py))
        
class MouseMallet(Mallet):
    
    def move(self, dt):
        
        touched = False
        self.friction(dt)
        old_px, old_py = self.get_pos_xy()
        puck_px, puck_py = self.get_puck().get_pos_xy()
        
        new_pos = pygame.mouse.get_pos()
        new_pos = Vector(angle_from_O(new_pos), distance_from_O(new_pos))
        new_px, new_py = new_pos.get_xy()
        px, py = self.get_pos_xy()
        vx = (new_px - px)/dt
        vy = (new_py - py)/dt
        
        self.set_speed_angle(angle_from_O((vx,vy)))
        new_speed = distance_from_O((vx,vy))
        if new_speed<=self.get_max_speed():
            self.set_speed_magnitude (new_speed)
            
        px,py = new_pos.get_xy()
        
        if (px < self.get_rink().get_left()+self.get_radius()):
            px = self.get_rink().get_left()+self.get_radius()
            touched = True
        elif (px > self.get_rink().get_right()-self.get_radius()):
            px = self.get_rink().get_right()-self.get_radius()
            touched = True
        
        if (py < self.get_top_bound()):
            py = self.get_top_bound()
            touched = True
        elif (py > self.get_bottom_bound()):
            py = self.get_bottom_bound()
            touched = True
        
        # Prevent from oscillating near the borders
        if touched:
            old_pos = self.get_pos_xy()
            self.set_speed_angle(angle(old_pos,(px,py)))
            self.set_speed_magnitude(distance(old_pos,(px,py))/dt)
            
        if self.overlaps():
            x = (old_px - puck_px) > 0
            px = old_px + x * 5
            y = (old_py - puck_py) > 0
            py = old_py + y * 5
        
        self.set_pos_xy((px, py))
        
        
class CpuMallet(Mallet):
    
    def __init__( self, player, rink, puck, color=colors['red'], radius=20, mass=20, max_speed=0.6, friction=0.0001, acceleration=0.0025):
        super().__init__(player, rink, puck, color, radius, mass, max_speed, friction, acceleration)
        self.__reachable_top_bound    = self.get_top_bound()    - self.get_radius()
        self.__reachable_bottom_bound = self.get_bottom_bound() + self.get_radius()
        self.__range = self.get_rink().get_width() // 4
        
    def intersects(self, origin, direction, line):
        v1 = origin - line[0]
        v2 = line[1] - line[0]
        v3 = np.array([-direction[1], direction[0]])
        t1 = np.cross(v2, v1) / np.dot(v2, v3)
        t2 = np.dot(v1, v3) / np.dot(v2, v3)
        if t1 >= 0.0 and t2 >= 0.0 and t2 <= 1.0:
            return [origin + t1 * direction]
        return None
        
    
    def move(self, dt):
        touched = False
        self.friction(dt)
        
        if self.get_player() == 'top':
            goal_line = np.array([(200, 30), (300, 30)])
            
            old_px, old_py = self.get_pos_xy()
            px, py = old_px, old_py
            vx, vy = self.get_speed_xy()
            
            puck = self.get_puck()
            puck_px, puck_py = puck.get_pos_xy()
            puck_vx, puck_vy = puck.get_speed_xy()
            
            intersects = self.intersects(np.array((puck_px, puck_py)), np.array((puck_vx, puck_vy)), goal_line)
            if intersects != None:
                goal_px, goal_py = intersects[0]
            else:
                goal_px, goal_py = (250, 30)
            
            x, y = 0, 0
            reachable = self.__reachable_top_bound <= puck_py <=  self.__reachable_bottom_bound
            if not reachable:
                self.set_acceleration(0.0025)
                x = random.randrange(-1, 2, 1)
                y = random.randrange(-1, 2, 1)
                
                if x == -1 and px < self.get_rink().get_left()   + self.get_radius() + self.__range*2: x = 1
                elif x == 1 and px > self.get_rink().get_right() - self.get_radius() - self.__range*2: x = -1
                if y == 1 and py > self.get_top_bound() + self.__range: y = -1
                
            else:
                if puck_vy > 0:
                    self.set_acceleration(0.015)
                    if puck_px < px:
                        x = -1
                    if puck_px > px:
                        x = 1
                    if puck_py < py:
                        y = -1
                    if puck_py > py:
                        y = 1
                else:
                    too_fast = puck.get_speed_magnitude() > 0.8 * puck.get_max_speed()
                    
                    if too_fast:
                        self.set_acceleration(0.008)
                        diff_px = goal_px - px
                        if abs(diff_px) < 5: x = 0
                        elif diff_px > 0:    x = 1
                        else:                x = -1
                        x *= min(abs(diff_px)/20, 1)
                    
                        diff_py = goal_py - py
                        if abs(diff_py) < 5: y = 0
                        elif diff_py > 0:    y = 1
                        else:                y = -1
                        y *= min(abs(diff_py)/20, 1)
                    else:
                        self.set_acceleration(0.015)
                        if puck_px < px:
                            x = -1
                        if puck_px > px:
                            x = 1
                        if puck_py < py:
                            y = -1
                        if puck_py > py:
                            y = 1
            
        else:
        
            goal_line = np.array([(200, 670), (300, 670)])
            
            old_px, old_py = self.get_pos_xy()
            px, py = old_px, old_py
            vx, vy = self.get_speed_xy()
            
            puck = self.get_puck()
            puck_px, puck_py = puck.get_pos_xy()
            puck_vx, puck_vy = puck.get_speed_xy()
            
            intersects = self.intersects(np.array((puck_px, puck_py)), np.array((puck_vx, puck_vy)), goal_line)
            if intersects != None:
    #            print('intersects')
                goal_px, goal_py = intersects[0]
            else:
                goal_px, goal_py = (250, 670)
            
            x, y = 0, 0
            reachable = self.__reachable_top_bound <= puck_py <=  self.__reachable_bottom_bound
            if not reachable:
                self.set_acceleration(0.0025)
                x = random.randrange(-1, 2, 1)
                y = random.randrange(-1, 2, 1)
                
                if x == -1 and px < self.get_rink().get_left()   + self.get_radius() + self.__range*2: x = 1
                elif x == 1 and px > self.get_rink().get_right() - self.get_radius() - self.__range*2: x = -1
                if y == -1 and py < self.get_bottom_bound() - self.__range: y = 1
                
            else:
                if puck_vy < 0:
                    self.set_acceleration(0.015)
                    if puck_px < px:
                        x = -1
                    if puck_px > px:
                        x = 1
                    if puck_py < py:
                        y = -1
                    if puck_py > py:
                        y = 1
                else:
                    too_fast = puck.get_speed_magnitude() > 0.8 * puck.get_max_speed()
                    
                    if too_fast:
                        self.set_acceleration(0.008)
                        diff_px = goal_px - px
                        if abs(diff_px) < 5: x = 0
                        elif diff_px > 0:    x = 1
                        else:                x = -1
                        x *= min(abs(diff_px)/20, 1)
                    
                        diff_py = goal_py - py
                        if abs(diff_py) < 5: y = 0
                        elif diff_py > 0:    y = 1
                        else:                y = -1
                        y *= min(abs(diff_py)/20, 1)
                    else:
                        self.set_acceleration(0.015)
                        if puck_px < px:
                            x = -1
                        if puck_px > px:
                            x = 1
                        if puck_py < py:
                            y = -1
                        if puck_py > py:
                            y = 1
            
                
        vx,vy = self.get_speed_xy()
        vx += x*self.get_acceleration()*dt
        vy += y*self.get_acceleration()*dt
        
        self.set_speed_angle(angle_from_O((vx,vy)))
        new_speed = distance_from_O((vx,vy))
        if new_speed<=self.get_max_speed():
            self.set_speed_magnitude (new_speed)
 
        new_pos = self.get_pos()+dt*self.get_speed()
        px, py = new_pos.get_xy()
        
        if (px < self.get_rink().get_left()+self.get_radius()):
            px = self.get_rink().get_left()+self.get_radius()
            touched = True
        elif (px > self.get_rink().get_right()-self.get_radius()):
            px = self.get_rink().get_right()-self.get_radius()
            touched = True
        
        if (py < self.get_top_bound()):
            py = self.get_top_bound()
            touched = True
        elif (py > self.get_bottom_bound()):
            py = self.get_bottom_bound()
            touched = True
            
        if self.overlaps():
            x = (old_px - puck_px) > 0
            px = old_px + x * 5
                
            y = (old_py - puck_py) > 0
            py = old_py + y * 5
                
        
        # Prevent from oscillating near the borders
        if touched:
            old_pos = self.get_pos_xy()
            self.set_speed_angle(angle(old_pos,(px,py)))
            self.set_speed_magnitude(distance(old_pos,(px,py))/dt)
        
        self.set_pos_xy((px, py))

        
    
