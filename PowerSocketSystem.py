import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm

"""
    System Setup
"""

# create 5 sockets in a fixed order
socket_order = [2,1,3,5,4]

# the true values of each socket
socket_means = [((q*2)+2) for q in socket_order]

# save the number of sockets
NUM_SOCKETS = len(socket_order)

"""
    Helper Functions
"""

# return the index of the largest value in the supplied list
# - arbitrarily select between the largest values in the case of a tie
# (the standard np.argmax just chooses the first value in the case of a tie)
def random_argmax(value_list):
  """ a random tie-breaking argmax"""
  values = np.asarray(value_list)
  return np.argmax(np.random.random(values.shape) * (values==values.max()))



class PowerSocket:
    """ the base power socket class """
    
    def __init__(self, q):                
        self.q = q   # the true reward value                
        self.Q = 0   # the estimate of this socket's reward value                
        self.n = 0   # the number of times this socket has been tried
    
    # the reward is a random distribution around the initial mean value set for this socket
    # - never allow a charge less than 0 to be returned
    def charge(self):
        # a guassian distribution with unit variance around the true value 'q'
        value = np.random.randn() + self.q        
        return 0 if value < 0 else value
                    
    # increase the number of times this socket has been used and improve the estimate of the 
    # value (the mean) by combining the new reward 'r' with the current mean
    def update(self,R):
        self.n += 1

        # the new estimate is calculated from the old estimate
        self.Q = (1 - 1.0/self.n) * self.Q + (1.0/self.n) * R

    # return the estimate of the socket's reward value
    def sample(self):
        return self.Q


# Create an Optimistic Power Socket class by inheriting from the standard Power Socket
class OptimisticPowerSocket( PowerSocket ):
    def __init__( self, q, initial_estimate = 0. ):    
        
        # pass the true reward value to the base PowerSocket             
        super().__init__(q)        
        
        # estimate of this socket's reward value 
        # - set to supplied initial value
        self.Q = initial_estimate                 
        
        # the number of times this socket has been tried 
        # - set to 1 if an initialisation value is supplied
        self.n = 1 if initial_estimate > 0 else 0                


class SocketTester():

    def __init__(self, socket=OptimisticPowerSocket, socket_order=socket_order, initial_estimate = 0. ):  
        
        # create the supplied socket type with a mean value defined by the socket order       
        self.sockets = [socket((q*2)+2, initial_estimate) for q in socket_order]                  
        
        # set the number of sockets equal to the number created
        self.number_of_sockets = len(self.sockets)           

        # the index of the best socket is the last in the socket_order list
        # - this is a one-based value so convert to zero-based
        self.optimal_socket_index = (socket_order[-1] - 1)     
        
        # store any initial estimate used to initialize the sockets
        self.initial_estimate = initial_estimate
                     
       
    def run( self, number_of_steps ):            
        
        # save data about the run to create a table of estimates
        estimates = np.zeros(shape=(number_of_steps+1, self.number_of_sockets))

        # set the first estimates to be the initial value
        estimates[0] = self.initial_estimate 

        # monitor the total reward obtained over the run
        total_reward = 0

        # monitor the number of times the optimal socket was chosen
        optimal_socket_selected = 0

        # keep a count of the number of times each socket was selected
        selected_socket = np.zeros(shape=(self.number_of_sockets))   
        
        # loop for the specified number of time-steps
        for t in range(number_of_steps):

            # select a socket
            socket_index = self.select_socket(t)

            # charge from the chosen socket and update its mean reward value
            reward = self.sockets[socket_index].charge()
            self.sockets[socket_index].update(reward)

            # store the estimates of each socket at this time step
            for socket_number in range(self.number_of_sockets):
                estimates[t+1,socket_number] = self.sockets[socket_number].Q 

            # update the total reward
            total_reward += reward

            # monitor the number of times the optimal socket was chosen
            if socket_index == self.optimal_socket_index: 
                optimal_socket_selected += 1      

            # increment the count of the number of times the selected socket has been used
            selected_socket[socket_index] += 1

        return estimates, (total_reward/number_of_steps), (optimal_socket_selected/number_of_steps), (selected_socket/number_of_steps)    
    
    
    def select_socket( self, t ):
        """ Greedy Socket Selection"""
        
        # choose the socket with the current highest mean reward or arbitrary select a socket in the case of a tie            
        socket_index = random_argmax([socket.sample() for socket in self.sockets])  
        
        return socket_index        