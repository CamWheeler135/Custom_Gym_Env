''' Constructing a Deep Q Agent That Plays GhostlyGridWorld.V0 '''

import gymnasium as gym
import tensorflow as tf
from tensorflow import keras
import numpy as np
import random


env = gym.make('ghostly_grid_world_v0')

print(env.action_space)

