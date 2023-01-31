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
        assert self.size >= 6, "Grid size must be equal to or above 5 to allow room for agent to move away from the ghosts."

        # Initialise the positions of each element in the world.
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(low=0, high=0, shape=(2, ), dtype=np.int32),
                "target": spaces.Box(low=size - 1, high=size - 1, shape=(2, ), dtype=np.int32),
                "ghost1": spaces.Box(low=2, high=size - 1, shape=(2, ), dtype=np.int32),
                "ghost2": spaces.Box(low=2, high=size - 1, shape=(2, ), dtype=np.int32)
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
        self.render_mode = 'human'
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
        self._ghost2_location = np.clip(self._ghost2_location + ghost_2_action, 0, self.size - 1)
    
        # If ghosts catch agent, or agent at target, we give reward appropriately and Done = True
        reward, done = self.get_reward()
        
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
            return -1, True
        elif np.array_equal(self._agent_location, self._target_location):
            return +1, True
        else: 
            return 0, False


    def reset(self):
        ''' 
        Resets the environment for a new episode.
        Returns a tuple of
        (Initial observation, Auxiliary information)
        ''' 

        # Set the location of sprites. 
        self._agent_location = self.observation_space["agent"].sample()
        self._ghost1_location = self.observation_space["ghost1"].sample()
        self._ghost2_location = self.observation_space["ghost2"].sample()
        self._target_location = self.observation_space["target"].sample()

        observation = self.get_observation()
        info = dict()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

        
    
    #  PyGame Code adapted from the OpenAI Gymnasium Tutorial https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/
    def render(self):
        ''' Renders the view of the game. '''
        if self.render_mode == "rgb_array":
            return self._render_frame()


    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_size, self.window_size))

        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        # Create the surface that we are working on.
        game_window = pygame.Surface((self.window_size, self.window_size))
        game_window.fill((54, 69, 79))
        square_size = self.window_size / self.size

        # # Render in the door.
        pygame.draw.rect(game_window,(0, 255, 0), pygame.Rect(square_size * self._target_location, (square_size, square_size)))
        # Render in the agent.
        pygame.draw.circle(game_window, (255, 0, 0), (self._agent_location + 0.5) * square_size, square_size / 3 )
        # Render in ghosts
        pygame.draw.circle(game_window, (0, 0, 255), (self._ghost1_location + 0.5) * square_size, square_size / 3 )
        pygame.draw.circle(game_window, (0, 0, 255), (self._ghost2_location + 0.5) * square_size, square_size / 3 )

        # Render in the grid lines
        for x in range(self.size+1):
            # draw the y axis
            pygame.draw.line(game_window, (255, 255, 255), (0, square_size * x), (self.window_size, square_size * x), width=3)
            # draw the x axis
            pygame.draw.line(game_window, (255, 255, 255), (square_size * x, 0), (square_size * x, self.window_size), width=3)


        if self.render_mode == "human":
            # The following line copies our drawings from game_window to the visible window
            self.window.blit(game_window, game_window.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(game_window)), axes=(1, 0, 2))

            
    def close(self):
        ''' Closes any open resources that the environment uses. '''
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()



#----- Testing -----#

# env = GhostlyGridWorld(size=6)
 
# for episode in range(10):
#     env.reset()
#     done = False 
#     while done == False:
#         obv, reward, done, info = env.step(action=np.random.randint(0, 4)) # Mimics random selection of agent action
#         print(f"Observation: {obv}, Reward: {reward}, Done: {done}, Info: {info}")
#     print(f"\n---- Episode reward: {reward} ----\n")

