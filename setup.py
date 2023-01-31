from setuptools import setup

setup(
    name="GhostlyGridWorld",
    version="0.0.1",
    description='A variation of the classic grid world environment where the agent must find a way to the terminal state, avoiding two ghosts that move randomly around the grid.',
    author='Cameron Wheeler',
    install_requires=["gymnasium", "pygame"],
)