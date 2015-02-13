import numpy as np

class LabelEncoder(object):
    def __init__(self):


class LinearSVM(object):
    def __init__(self, solve_type):
        self.solve_type = solve_type

    def fix(self, X, y):
        self.classes = np.unique(y)
        enc = LabelEncoder()
        y_ind = enc.fit_transform(y)
        classes_ = enc.classes_
        # LibLinear wants targets as doubles, even for classification
        y_ind = np.asarray(y_ind, dtype=np.float64).ravel()
