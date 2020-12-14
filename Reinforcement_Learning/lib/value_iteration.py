import numpy as np


''' implement the Value Iteration algorithm '''
class ValueIteration():    
  
  policy = None
    
  def __init__(self,level,discount_factor=0.9):
    self.level = level    
    self.maze = level.maze
    self.values = np.zeros((level.height,level.width))
    self.discount_factor = discount_factor       
    
  def get_state_value(self,pos):
    ''' get the currently calculated value of the specified position in the grid '''
    x = pos[0]
    y = pos[1]
    if (x < 0 or x >= self.level.width) or (y < 0 or y >= self.level.height): return 0
    return self.values[y,x]    
    
  def get_available_actions(self,x,y):
    ''' return the list of available actions for the specified position in the grid '''
    
    # test if the level contains a maze
    if self.maze is not None:        
      cell = self.maze.cell_at( x, y )  
      
      # if a wall is present then that direction is not possible as an action
      actions = {k: not v for k, v in cell.walls.items()}      
    else:
      # initially start with all actions being possible
      actions = {'N':True,'E':True,'S':True,'W':True}

      # if the center area is not part of the level then remove any actions that would move there
      if self.level.fill_center == True:
        if ((x >= 1 and x <= self.level.width-2) and (y >= 1 and y <= self.level.height-2)): 
          actions = {}
        else:
          if ((x >= 1 and x <= self.level.width-2) and (y == 0)): del actions['S'] 
          elif ((x >= 1 and x <= self.level.width-2) and (y == self.level.height-1)): del actions['N'] 
          elif ((y >= 1 and y <= self.level.height-2) and (x == 0)): del actions['E']             
          elif ((y >= 1 and y <= self.level.height-2) and (x == self.level.width-1)): del actions['W']
            
      # remove actions that would move off the edges of the grid
      if x == 0: del actions['W']
      if x == self.level.width-1: del actions['E']
      if y == 0: del actions['N']
      if y == self.level.height-1: del actions['S']     
      
    # test if a policy has been defined
    if self.policy is not None:
      # set any allowed actions to false if they're not in the policy
      dir_value = self.policy[y,x]
      for direction,v in actions.items():        
        if v == True:
          if (direction == 'N') and not (dir_value & Direction.North): actions['N'] = False
          if (direction == 'S') and not (dir_value & Direction.South): actions['S'] = False
          if (direction == 'E') and not (dir_value & Direction.East):  actions['E'] = False
          if (direction == 'W') and not (dir_value & Direction.West):  actions['W'] = False      
      
    return actions
  
  def calculate_max_action_value(self,x,y):
    ''' calculate the values of all actions in the specified cell and return the largest of these '''
    
    # get the list of available actions for this cell
    actions = self.get_available_actions(x,y)
    
    # check that some actions are possible in this state
    if not actions: return 0        
    
    # calculate the value of each action in the state and save the largest
    max_value = float('-inf')
    for direction,v in actions.items():
      # test the action is allowed
      if v == True:                

        # calculate the postion of the next state
        next_pos = []        
        if direction == 'N': next_pos = [x,y-1]
        if direction == 'S': next_pos = [x,y+1]
        if direction == 'E': next_pos = [x+1,y]
        if direction == 'W': next_pos = [x-1,y]

        # always -1 for taking an action
        value = -1 + (self.discount_factor * self.get_state_value( next_pos ))
        
        # save the largest value
        if value > max_value:
          max_value = value              
    
    # return the value of the largest action-value in this state
    return max_value  
  

  def state_sweep(self):
    ''' calculate the value of all states except the exit '''
    
    new_values = np.zeros((self.level.height,self.level.width))
    end = self.level.get_end()    
    for y in range(self.level.height):
      for x in range(self.level.width):
        if (x != end[0]) or (y != end[1]):
          new_values[y,x] = self.calculate_max_action_value(x,y)    

    # calculate the largest difference in the state values between the start and end of the sweep
    delta = np.max(np.abs(new_values - self.values))           
    
    # update the state values with the newly calculated values
    self.values = new_values

    # return the largest state value difference 
    return delta

  
  def run_to_convergence(self, max_iterations = 100, threshold = 1e-3):
    ''' run multiple state sweeps until the maximum change in the state value falls
        below the supplied threshold or the maximum number of iterations is reached
    '''
    
    for n in range(max_iterations):
      
      # calculate the maximum action value in each state and get the largest state value difference
      delta = self.state_sweep()        
      
      # test if the difference is less than the defined convergence threshold
      if delta < threshold:
        break
    
    # return the number of iterations taken to converge
    return n