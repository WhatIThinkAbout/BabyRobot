import numpy as np
from direction import Direction

class Policy():
  
  def __init__(self,level):
    self.level = level
    self.maze = level.maze
    self.directions = np.zeros((level.height,level.width),dtype=np.int)
    
  def set_policy(self,directions):
    ''' set the policy (i.e. the action to take in each state) '''
    self.directions = directions
    
  def get_policy(self):
    return self.directions
    
  def get_directions(self,values):
    self.directions = self.calculate_greedy_directions(values)
    return self.directions
  
  def update_policy(self,values):
    # if greedy policy specifies more than one action for a state select the action
    # that was in previous policy
    
    greedy_directions = self.calculate_greedy_directions(values)

    for row in range(self.directions.shape[0]):
      for col in range(self.directions.shape[1]):    
        # if a single direction is specified the value will be a power of 2
        n = greedy_directions[row,col]  
        power_of_two = (n & (n-1) == 0) and n != 0   
        if not power_of_two:      
          # more than one direction so use direction from last policy
          greedy_directions[row,col] = self.directions[row,col]    
          
    # update the policy
    self.directions = greedy_directions
    return self.directions
  
  
  def calculate_greedy_directions(self,values):    
    # calculate the directions of all states except the exit  
    directions = np.zeros((self.level.height,self.level.width),dtype=np.int)
    end = self.level.get_end()  
    for y in range(self.level.height):
      for x in range(self.level.width):
        if (x != end[0]) or (y != end[1]):
          directions[y,x] = self.calculate_cell_directions(x,y,values)    
    return directions
          
  def calculate_cell_directions(self,x,y,values):
    actions = self.level.get_available_actions(x,y)
    
    directions = 0
    dir_value = 0
    best_value = -1000000
    for direction,v in actions.items():
      # test the action is allowed
      if v == True:                  
        
        # calculate the postion of the next state              
        if direction == 'N': value = values[y-1,x]; dir_value = Direction.North          
        if direction == 'S': value = values[y+1,x]; dir_value = Direction.South  
        if direction == 'E': value = values[y,x+1]; dir_value = Direction.East  
        if direction == 'W': value = values[y,x-1]; dir_value = Direction.West  
          
        if value > best_value: 
          directions = dir_value
          best_value = value
        elif value == best_value: directions += dir_value
                
    return int(directions)

  
  def get_allowed_actions(self,x,y):
    ''' return a list of the allowed actions for the specified state '''
    
    allowed_actions = []
    
    # no more actions once we reach the exit
    end = self.level.get_end()    
    if x != end[0] or y != end[1]:    
    
      # get the actions available for the level
      actions = self.level.get_available_actions(x,y)    

      for direction,v in actions.items():
        # test the action is allowed
        if v == True:                  

          # calculate the postion of the next state              
          if direction == 'N': allowed_actions.append( Direction.North )
          if direction == 'S': allowed_actions.append( Direction.South ) 
          if direction == 'E': allowed_actions.append( Direction.East )  
          if direction == 'W': allowed_actions.append( Direction.West )
          
    return allowed_actions   