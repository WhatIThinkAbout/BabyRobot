import numpy as np
from direction import Direction


''' evaluate a policy '''
class PolicyEvaluation():
  
  iterations = 0
  policy = None
  discount_factor = 1
  
  def __init__(self,level,discount_factor = 1):
    self.level = level
    self.maze = level.maze
    self.start_values = np.zeros((level.height,level.width))
    self.end_values = np.zeros((level.height,level.width))
    self.discount_factor = discount_factor
    
  def reset(self):
    self.iterations = 0
    self.start_values = np.zeros((level.height,level.width))
    self.end_values = np.zeros((level.height,level.width))    

  def show_start_values(self):
    print(self.start_values)
    
  def show_end_values(self):
    print(self.end_values)   
    
  def get_iterations(self):
    return self.iterations
    
  def standard_sweep(self):
    
    # the exit always has a value of zero
    end = self.level.get_end()    
    
    # calculate the value of all states except the exit
    for y in range(self.level.height):
      for x in range(self.level.width):
        if (x != end[0]) or (y != end[1]):
          self.end_values[y,x] = self.calculate_cell_value(x,y)   
        
        
  def do_iteration(self):        
    self.start_values = self.end_values                      # copy the end values into the start values            
    self.end_values = np.zeros((self.level.height,self.level.width))   # reset the end values        
    self.standard_sweep()                                    # sweep all states    
    self.iterations += 1                                     # increment the iteration count
    
  def run_to_convergence(self, max_iterations = 100, threshold = 1e-3):
    ''' run until the values stop changing '''
    for n in range(max_iterations):
      self.do_iteration()
      
      # calculate the largest difference in the state values from the start to end of the iteration
      delta = np.max(np.abs(self.end_values - self.start_values))            
      
      # test if the difference is less than the defined convergence threshold
      if delta < threshold:
        break
    
    # return the number of iterations taken to converge
    return n
      
        
  def get_state_value(self,pos):
    x = pos[0]
    y = pos[1]
    if (x < 0 or x >= self.level.width) or (y < 0 or y >= self.level.height): return 0
    return self.start_values[y,x]
        
  def calculate_cell_value(self,x,y):
    actions = self.get_available_actions(x,y)
    
    # check that some actions are possible in this state
    if not actions: return 0
    
    num_actions = 0
    value = 0
    for direction,v in actions.items():
      # test the action is allowed
      if v == True:
        num_actions += 1                

        # calculate the postion of the next state
        next_pos = []        
        if direction == 'N': next_pos = [x,y-1]
        if direction == 'S': next_pos = [x,y+1]
        if direction == 'E': next_pos = [x+1,y]
        if direction == 'W': next_pos = [x-1,y]

        # always -1 for taking an action
        value += -1 + (self.discount_factor * self.get_state_value( next_pos ))

    # check that some action was taken
    if not num_actions: return 0        

    # for equal probability of taking an action its just the mean of all actions
    return value/num_actions    
    
  def get_available_actions(self,x,y):
    # test if the level contains a maze
    if self.maze is not None:        
      cell = self.maze.cell_at( x, y )  
      
      # if a wall is present then that direction is not possible as an action
      actions = {k: not v for k, v in cell.walls.items()}      
    else:
      actions = {'N':True,'E':True,'S':True,'W':True}
      if self.level.fill_center == True:
        if ((x >= 1 and x <= self.level.width-2) and (y >= 1 and y <= self.level.height-2)): 
          actions = {}
        else:
          if ((x >= 1 and x <= self.level.width-2) and (y == 0)): del actions['S'] 
          elif ((x >= 1 and x <= self.level.width-2) and (y == self.level.height-1)): del actions['N'] 
          elif ((y >= 1 and y <= self.level.height-2) and (x == 0)): del actions['E']             
          elif ((y >= 1 and y <= self.level.height-2) and (x == self.level.width-1)): del actions['W']
            
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
  
  def set_policy(self,policy):
    ''' set the policy to be evaluated '''
    self.policy = policy
    
    # reset the iterations required to run to convergence on the policy
    self.iterations = 0
    
  def set_discount_factor(self, discount_factor):
    ''' set the discount factor to apply to the future rewards '''
    self.discount_factor = discount_factor     