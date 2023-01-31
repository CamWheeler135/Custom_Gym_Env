''' Constructing a Deep Q Agent That Plays GhostlyGridWorld.V0 '''

import gymnasium as gym
import tensorflow as tf
from tensorflow import keras
import numpy as np
import ghostly_grid

env = gym.make('ghostly_grid/GhostlyGridV0')

print(env.action_space)
print(env.observation_space)
