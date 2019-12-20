import random
import time
from operator import itemgetter

from reinforcmentlearning.models.deep_learning_model import DeepLearningModel
from reinforcmentlearning.models.lookup_table_model import LookupTableModel


class QAlgorithmController:
    def __init__(self, environment, algorithm_configuration, is_deep_learning=False) -> None:
        super().__init__()
        self.environment = environment
        self.algorithm_configuration = algorithm_configuration
        self.current_epsilon = algorithm_configuration.epsilon
        self.model = DeepLearningModel(self.environment) if is_deep_learning else LookupTableModel(self.environment)

    def reset_model(self, is_deep_learning=False):
        self.model = DeepLearningModel(self.environment) if is_deep_learning else LookupTableModel(self.environment)

    def train(self, number_of_games):
        scores = []
        best_score = 0
        for i in range(number_of_games):
            current_state = self.environment.reset()
            sum_reward = 0
            while True:
                new_state, reward, is_done, = self.train_one_round(current_state)
                current_state = new_state
                sum_reward = sum_reward + reward
                if is_done:
                    break
            scores.append(sum_reward)
            if sum_reward > best_score:
                best_score = sum_reward
        print('Average after  ', number_of_games, ' games : ', sum(scores) / len(scores))
        print('Best score : ', best_score)
        self.environment.close()

    def train_and_render(self, number_of_games):
        scores = []
        best_score = 0
        for i in range(number_of_games):
            current_state = self.environment.reset()
            sum_reward = 0
            while True:
                time.sleep(0.1)
                self.environment.render()
                new_state, reward, is_done, = self.train_one_round(current_state)
                current_state = new_state
                sum_reward = sum_reward + reward
                if is_done:
                    break
            scores.append(sum_reward)
            if sum_reward > best_score:
                best_score = sum_reward
            print('Game score : ', sum_reward)
        print('Average after  ', number_of_games, ' games : ', sum(scores) / len(scores))
        print('Best score : ', best_score)
        self.environment.close()

    def play_random(self, number_of_games):
        scores = []
        best_score = 0
        for i in range(number_of_games):
            current_state = self.environment.reset()
            sum_reward = 0
            while True:
                new_state, reward, is_done, = self.play_random_round(current_state)
                current_state = new_state
                sum_reward = sum_reward + reward
                if is_done:
                    break
            if sum_reward > best_score:
                best_score = sum_reward
            scores.append(sum_reward)
        print('Average after  ', number_of_games, ' games : ', sum(scores) / len(scores))
        print('Best score : ', best_score)
        self.environment.close()

    def play_random_round(self, state):

        current_action = self.environment.get_random_action()

        new_state, reward, is_done, _ = self.environment.perform_action(state, current_action)

        return new_state, reward, is_done

    def train_one_round(self, state):

        current_action = self._get_current_action(state)

        new_state, reward, is_done, _ = self.environment.perform_action(state, current_action[0])

        current_q_value = current_action[1]

        if is_done:
            reward = self.environment.get_game_over_reward()

        new_q_value = self._calculate_new_q_value(current_q_value, reward, new_state)

        self.model.update_state(state, current_action[0], new_q_value)

        if self.current_epsilon >= self.algorithm_configuration.epsilon_min:
            self.current_epsilon = self.current_epsilon * self.algorithm_configuration.epsilon_decay

        return new_state, reward, is_done

    def _calculate_new_q_value(self, current_q_value, reward, new_state):
        new_state_actions = self.model.predict(new_state)
        best_action_value_tuple = max(new_state_actions.items(), key=itemgetter(1))
        return ((
                        1 - self.algorithm_configuration.learning_rate) * current_q_value) + self.algorithm_configuration.learning_rate * (
                       reward + (self.algorithm_configuration.gamma * best_action_value_tuple[1]))

    def _get_current_action(self, state):
        random_value = random.random()
        current_actions = self.model.predict(state)

        if random_value <= self.current_epsilon:
            random_action = random.choice(list(current_actions))
            return random_action, current_actions[random_action]
        else:
            return max(current_actions.items(), key=itemgetter(1))
