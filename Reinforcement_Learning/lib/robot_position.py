import grid_level
from direction import Direction
import threading
from time import sleep, time
import random

from ipycanvas import MultiCanvas
from ipycanvas import Canvas, hold_canvas
from ipywidgets import Image
from ipywidgets import Layout
from ipywidgets import Play, IntProgress, HBox, VBox, link

import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)


''' control robot positioning and drawing '''
class RobotPosition():
    
    sprite_count = 0
    move_count = 0   
    canvas_sprites = []

    
    def __init__(self, level, x_size = 256, y_size = 256, initial_sprite = 4, start_pos = None):
        
        self.level = level
        self.canvas = level.canvases[2]
        self.maze = level.maze
                                
        self.x = 0
        self.y = 0     
        self.step = 4
        self.robot_size = 64
        
        # the number of steps before a sprite change
        self.sprite_change = 2
        
        if self.maze is None:
            self.x_size = level.width_pixels
            self.y_size = level.height_pixels
        else:
            x,y = self.maze.dimensions()
            self.x_size = x * self.robot_size
            self.y_size = y * self.robot_size
                       
        self.sprite_index = initial_sprite        
        self.load_sprites()              
        
        if not start_pos:
          self.set_cell_position(level.start)
        else:
          self.set_cell_position(start_pos)
        
    def get_number_of_sprites(self):
        return len(self.canvas_sprites)
    
    def get_cell_position(self):
        return self.x//self.robot_size, self.y//self.robot_size
           
    def set_cell_position(self, *args):
      ''' set the robot position in pixels '''
      if len(args) == 1:    
        self.x,self.y = self.level.grid_to_pixels(args[0])
      elif len(args) == 2: 
        self.x,self.y = self.level.grid_to_pixels([args[0],args[1]])      
        
    def get_array(self,*args, **kwargs):                
        ' callback to split the sprite sheet into individual sprites '        

        # check that the sprites haven't already been created
        if self.get_number_of_sprites() == 0:
            index = 0
            for row in range(5):
                for col in range(2):                                 
                    x = col * (self.robot_size + 1)                    
                    y = row * (self.robot_size + 1)
            
                    # copy the sprite from the sprite sheet
                    image_data = self.sprite_canvas.get_image_data( x, y, self.robot_size)

                    # put the sprite onto its own canvas
                    canvas = Canvas(width=self.robot_size, height=self.robot_size)
                    canvas.put_image_data( image_data, 0, 0 )  
                    self.canvas_sprites.append( canvas )
        
        # add a sprite to the display
        self.canvas.clear()
        self.draw()     
        
    def load_sprites(self):        
        ' load the sprite sheet and when loaded callback to split it into individual sprites '        
        sprites = Image.from_file('images/BabyRobot64_Sprites.png')
        self.sprite_canvas = Canvas(width=132, height=328, sync_image_data=True)           
        self.sprite_canvas.draw_image( sprites, 0, 0 )                 
        self.sprite_canvas.observe(self.get_array, 'image_data')              
            
    def update_sprite(self):
        ' randomly change to the next sprite '        
        self.sprite_count += 1
        if self.sprite_count > self.sprite_change: 
            self.sprite_count = 0   
            self.sprite_index = self.sprite_index + random.randint(-1,+1)   
            if self.sprite_index < 0: 
                self.sprite_index = 0
            if self.sprite_index >= self.get_number_of_sprites():
                self.sprite_index = (self.get_number_of_sprites()-1)    
                              
    def draw_sprite(self,index):   
        ' remove the last sprite and add the new one at the current position '
        if self.sprite_index < self.get_number_of_sprites():
            with hold_canvas(self.canvas):
                self.canvas.clear_rect(self.x, self.y, self.robot_size)                        
                self.canvas.draw_image(self.canvas_sprites[index], self.x, self.y )                       
        
    def draw(self):    
        ' add the current sprite at the current position '     
        self.draw_sprite(self.sprite_index)
        self.update_sprite()               
            
    def move(self,direction):        
        ' move from one square to the next in the specified direction '
        
        # check that the image sprites have been loaded
        if self.get_number_of_sprites() > 0:
            cell = None
            if self.maze is not None:
                x, y = self.get_cell_position()
                cell = self.maze.cell_at( x, y )            
                if direction == Direction.North and cell.walls['N']: return
                if direction == Direction.South and cell.walls['S']: return
                if direction == Direction.East and cell.walls['E']: return
                if direction == Direction.West and cell.walls['W']: return
            
            move_method_name = f"move_{direction.name}"        
            for step in range(self.robot_size//self.step):
                getattr(self,move_method_name)()  
                self.draw()  
                sleep(0.10) # pause between each move step        
                
            self.move_count += 1
        
    def partial_move(self,direction):        
        ' move from one square to the next in the specified direction '
                
        move_method_name = f"move_{direction.name}"        
        getattr(self,move_method_name)()  
        self.draw()  
            
        self.move_count += 1        
        
        
    def move_East(self):        
        if self.x < (self.x_size - self.robot_size):
            self.x += self.step
            
    def move_West(self):
        if self.x > 0: 
            self.x -= self.step            
            
    def move_North(self):
        if self.y > 0:           
            self.y -= self.step
            
    def move_South(self):
        if self.y < (self.y_size - self.robot_size):
            self.y += self.step