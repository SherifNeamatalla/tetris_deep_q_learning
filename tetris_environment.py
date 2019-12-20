import gym_tetris
from matplotlib import pyplot as plt

from reinforcmentlearning.environment.environment import Environment


class TetrisEnvironment(Environment):

    def __init__(self) -> None:
        super().__init__()
        self.env = gym_tetris.make('TetrisA-v0')

    def perform_action(self, state, action):
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def get_possible_states(self):
        result = list()
        self.env.reset()
        self.env.render()

        new_state = self.env.step(self.env.action_space.sample())
        self.env.render()

        plt.imshow(new_state, interpolation="nearest")

        return result

    def get_random_action(self):
        return self.env.action_space.sample()

    def get_state_id(self, state):
        pass

    def get_possible_actions(self):
        return self.env.action_space

    def render(self):
        return self.env.render()

    def close(self):
        return self.env.close()

    def get_game_over_reward(self):
        return -5
