from setuptools import setup

setup(
    name="ghostly_grid_world",
    version="0.0.1",
    description='A variation of the classic grid world environment where the agent must find a way to the terminal state, avoiding two ghosts that move randomly around the grid.',
    author='Cameron Wheeler',
    install_requires=["gymnasium==0.26.0", "pygame==2.1.0"],
)