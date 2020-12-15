import numpy as np
from grid_level import GridLevel


''' implement the Value Iteration algorithm '''
class ValueIteration():    
  
  policy = None
    
  def __init__(self,level,discount_factor=0.9):
    self.level = level        
    self.values = np.zeros((level.height,level.width))
    self.discount_factor = discount_factor       
    
  def get_state_value(self,pos):
    ''' get the currently calculated value of the specified position in the grid '''
    x = pos[0]
    y = pos[1]
    if (x < 0 or x >= self.level.width) or (y < 0 or y >= self.level.height): return 0
    return self.values[y,x]    
  
  def calculate_max_action_value(self,x,y):
    ''' calculate the values of all actions in the specified cell and return the largest of these '''
    
    # get the list of available actions for this cell
    actions = self.level.get_available_actions(x,y,self.policy)
    
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