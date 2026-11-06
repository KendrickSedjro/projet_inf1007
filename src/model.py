import pandas as pd
from abc import abstractmethod

class Model:
    def __init__(self, dataframe: pd.DataFrame):
        self.X = None
        self.y = None
        self.model = None

    @abstractmethod
    def train(self):
        pass

    def predict(self):
        pass

    def metrics(self):
        pass

    def plot_model(self):
        pass

    def save_model(self):
        pass


class RandomForest(Model): 
    def __init__(self):
        super().__init__()

    def train(self):
        pass



"""
A voir si on a le temps

class DecisionTree(Model): 
    def __init__(self):
        super().__init__()

    def train(self):
        pass
"""
