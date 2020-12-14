
from direction import Direction

class Arrows():
  ''' draw arrows to show policies '''
  
  a_width = 6
  a_height = 7
  line_length = 14
  
  def __init__(self,cell_pixels,padding,length=14,width=6,height=7):
    self.cell_pixels = cell_pixels
    self.padding = padding
    self.calculate_positions()
    self.line_length = length
    self.a_width = width
    self.a_height = height
    
  def set_center(self,x,y):
    ''' set the center of the tile '''
    self.cx = x + self.start
    self.cy = y + self.start     
    
  def calculate_positions(self):
    ''' calculate the number of pixels to center of a square '''
    self.start = self.cell_pixels//2 - self.padding
    
  def draw_horz_line(self,canvas,shift):
    canvas.begin_path()     
    canvas.move_to(self.cx + shift,self.cy)
    canvas.line_to(self.cx + shift + self.line_length,self.cy)     
    canvas.stroke()     
    
  def draw_vert_line(self,canvas,shift):
    canvas.begin_path()     
    canvas.move_to(self.cx,self.cy + shift)
    canvas.line_to(self.cx,self.cy + shift + self.line_length )      
    canvas.stroke()              
    
  def draw_vert_arrow(self,canvas,y1,y2):
    canvas.begin_path()
    canvas.move_to(self.cx, y2)
    canvas.line_to(self.cx + self.a_width, y1)
    canvas.line_to(self.cx - self.a_width, y1)
    canvas.fill() 
    
  def draw_horz_arrow(self,canvas,x1,x2):
    canvas.begin_path()
    canvas.move_to(x2, self.cy)
    canvas.line_to(x1, self.cy + self.a_width)
    canvas.line_to(x1, self.cy - self.a_width)
    canvas.fill()            
    
  def draw_arrow(self,canvas,x,y,direction):
    
    if direction == Direction.North: 
      y1 = self.cy - self.line_length + 1
      y2 = y1 - self.a_height + 1
      self.draw_vert_line(canvas,-self.line_length+1)
      self.draw_vert_arrow(canvas,y1,y2)
      
    if direction == Direction.South:       
      y1 = self.cy + self.line_length - 1
      y2 = y1 + self.a_height - 1       
      self.draw_vert_line(canvas,-1)   
      self.draw_vert_arrow(canvas,y1,y2)
      
    if direction == Direction.East:  
      x1 = self.cx + self.line_length - 1
      x2 = x1 + self.a_height - 1      
      self.draw_horz_line(canvas,-1)
      self.draw_horz_arrow(canvas,x1,x2)     
      
    if direction == Direction.West:  
      x1 = self.cx - self.line_length + 1
      x2 = x1 - self.a_height + 1     
      self.draw_horz_line(canvas,-self.line_length+1)     
      self.draw_horz_arrow(canvas,x1,x2)           
    
  def draw(self,canvas,x,y,directions,color='#000',center_width = 36):   
    
    canvas.line_width = 3
    canvas.fill_style = color
    canvas.stroke_style = color      
    
    self.set_center(x,y)    
    for direction in directions:          
      self.draw_arrow(canvas,x,y,direction)  
    
    # if a center width is defined then clear this area    
    if center_width > 0: 
      center_start = center_width//2
      canvas.clear_rect(self.cx-center_start,self.cy-center_start,center_width,center_width) 