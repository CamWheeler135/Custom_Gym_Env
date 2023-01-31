from gymnasium.envs.registration import register

register(
    id='ghostly_grid/GhostlyGridV0',
    entry_point='ghostly_grid.envs:GhostlyGridWorld'
)