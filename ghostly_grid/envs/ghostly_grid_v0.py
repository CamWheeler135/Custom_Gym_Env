# Here is where the environment will go.
import numpy as np
import gymnasium as gym
from gym import spaces
import pygame


class GhostlyGridWorld(gym.Env):
    ''' 
    A variation of OpenAIs Gym Grid world. 
    The environment is a 2D square that is specified with a size parameter (there is a minimum value as I want to provide enough room so that the agent can "run away" if it needs to).
    The agent can move up down left and right from the starting position [0, 0].
    The ghosts can move up down left and right, these are spawned in randomly at the start of each episode.
    The goal fo the agent is to reach the terminal square (the door) at the bottom right of the square [size, size].

    In this variation the agent can observe the whole environment, the location of the door, the location of the ghosts and the location of itself. 
    The done signal is issued as soon as the agent gets to the target, or if the ghosts catch the agent. 
    Rewards are 0 for each move, -1 for being caught and +1 for reaching the door.
    '''

    # Metadata.
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, size=6, render_mode=None) -> None:

         # Size of the grid world. 
        self.size = size
        assert self.size >= 7, "Grid size must be above 7 to allow room for agent to move."

        # Initialise the positions of each element in the world.
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(low=0, high=0, shape=(2, ), dtype=np.int32),
                "target": spaces.Box(low=size-1, high=size - 1, shape=(2, ), dtype=np.int32),
                "ghost1": spaces.Box(low=0, high=size - 1, shape=(2, ), dtype=np.int32),
                "ghost2": spaces.Box(low=0, high=size - 1, shape=(2, ), dtype=np.int32)
            }
        )
        self.action_space = spaces.Discrete(4)
        self.action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1])
        }

        # Rendering from the OpenAI Documentation
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window_size = 512
        self.window = None
        self.clock = None


    def step(self, action):
        ''' 
        Accepts an action and computes the transition of the environment
        after applying that action.
        Returns a tuple of 
        (Observation, Reward, Done, Info)
        '''

        # Convert the action into a direction in the grid world.
        agent_action = self.action_to_direction[action]
        ghost_1_action = self.action_to_direction[np.random.randint(0, 4)] # Move the ghosts at random around the world.
        ghost_2_action = self.action_to_direction[np.random.randint(0, 4)]

        # Move the agent and ghosts.
        self._agent_location = np.clip(self._agent_location + agent_action, 0, self.size - 1)
        self._ghost1_location = np.clip(self._ghost1_location + ghost_1_action, 0, self.size - 1)
        self._ghost2_location = np.clip(self._ghost1_location + ghost_2_action, 0, self.size - 1)
    
        # If ghosts catch agent, or agent at target we give reward appropriately and Done = True
        reward = self.get_reward()
        if reward == (+1 or -1):
            done = True
        else: 
            done=False
        
        # Get the observation
        observation = self.get_observation()
        info = dict()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, done, info


    def get_observation(self):
        ''' Gets observations at each time step. '''

        return {"agent": self._agent_location, "ghost1": self._ghost1_location, "ghost2": self._ghost2_location, "target": self._target_location}


    def get_reward(self):
        ''' Gets reward considering if the agent is in the terminal location, been caught or neither. '''

        if np.array_equal(self._agent_location, self._ghost1_location) or np.array_equal(self._agent_location, self._ghost2_location):
            return -1
        elif np.array_equal(self._agent_location, self._target_location):
            return +1
        else: 
            return 0


    def reset(self):
        ''' 
        Resets the environment for a new episode.
        Returns a tuple of
        (Initial observation, Auxiliary information)
        ''' 

        # Locations of sprites
        self._agent_location = self.observation_space["agent"].sample()
        self._ghost1_location = self.observation_space["ghost1"].sample()
        self._ghost2_location = self.observation_space["ghost2"].sample()
        self._target_location = self.observation_space["target"].sample()
        


    def render(self):
        ''' Renders the view of the game. '''
        pass

    def close(self):
        ''' Closes any open resources that the environment uses. '''



#----- Testing -----#

env = GhostlyGridWorld(8)

env.reset()

for i in range(200):
    obv, reward, done, info = env.step(action=np.random.randint(0, 4))
    print(f"Observation: {obv}, Reward: {reward}, Done: {done}, Info: {info}")

