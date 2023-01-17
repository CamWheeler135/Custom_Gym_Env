from gymnasium.envs.registration import register

register(
    id='GhostlyGrid-v0',
    entry_point='ghostlygrid.envs:GhostlyGridv0'
)