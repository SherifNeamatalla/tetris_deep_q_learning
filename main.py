from reinforcmentlearning.algorithm.algorithm_configuration import AlgorithmConfiguration
from reinforcmentlearning.algorithm.q_algorithm_controller import QAlgorithmController
from tetris_environment import TetrisEnvironment

environment = TetrisEnvironment()
algorithm_configuration = AlgorithmConfiguration(0.4, 1, 0.4, 0.99993, 0.005)
controller = QAlgorithmController(environment, algorithm_configuration)



controller.train_and_render(100)
