# Custom_Gym_Env

Creating my own custom OpenAi Gym Environment to practice the creation of environments for reinforcement learning. Here I will be implementing my twist on the classic Frozen-Lake grid world environment called "Ghostly Grid World", the aim of this project is to develop a deeper understanding of how RL environments work as I read through Miguel Morales Deep Reinforcement Learning book. 

This env works like a frozen lake, where an agent (Timmy) is trying to escape a haunted house through the door (positive terminal state). However, instead of having set "holes" (negative terminal states) in the environment, I would like to see how Timmy performs when "ghosts" move around. Ideally, like in the frozen lake env, Timmy will learn to make his way to the door and avoid the ghosts on his way. 

### References

- [Gymnasium Docs](https://gymnasium.farama.org).

- I have adapted the code from the OpenAI tutorial that runs through how to create a simple grid world with no negative terminal states, the agent just has to find the end goal. [OpenAI Gymnasium Tutorial](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/).

- The tutorial utilized pygame to render how the agent is playing, the tutorial referenced above, but the [Pygame Docs](https://www.pygame.org/docs/ref/draw.html#pygame.draw.line) contains much more information into how the code is working.

- A brief video walk through on how Gym envs should work by [Nicholas Renotte](https://www.youtube.com/watch?v=bD6V3rcr_54).
