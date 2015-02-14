import numpy as np

import liblinear


class LabelEncoder(object):
    def __init__(self):
        pass

    def fit_transform(self, y):
        self.classes_, y = np.unique(y, return_inverse=True)
        return y

    def inverse_transform(self, y):
        y = np.asarray(y)
        return self.classes_[y]


class LinearSVM(object):
    def __init__(self, solver_type, C=1.0, tol=1e-4, fit_intercept=True, intercept_scaling=1., dual=True,
                 verbose=0, random_state=None, max_iter=1000):
        self.solver_type = solver_type
        self.C = C
        self.tol = tol
        self.fit_intercept = fit_intercept
        self.intercept_scaling = intercept_scaling
        self.dual = dual
        self.verbose = verbose
        self.random_state = random_state
        self.max_iter = max_iter

    def fit(self, X, y, epsilon=0.1):
        enc = LabelEncoder()
        y_ind = enc.fit_transform(y)
        classes_ = enc.classes_
        # LibLinear wants targets as doubles, even for classification
        y_ind = np.asarray(y_ind, dtype=np.float64).ravel()
        class_weight_ = np.ones(classes_.shape[0], dtype=np.float64, order='C')
        bias = -1.0
        raw_coef_, n_iter_ = liblinear.train_wrap(X, y_ind, self.solver_type, 0, self.tol, bias, self.C,
                                                  class_weight_, self.max_iter, 0, epsilon)

        n_iter_ = max(n_iter_)
        return raw_coef_, n_iter_


if __name__ == '__main__':
    svm = LinearSVM(solver_type=4)
    X = np.ones((2, 5), dtype=np.float64)
    y = np.asarray([1, 1])
    svm.fit(X, y)