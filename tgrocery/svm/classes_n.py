import numpy as np

import liblinear


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
        # LibLinear wants targets as doubles, even for classification
        y = np.asarray(y, dtype=np.float64).ravel()
        classes_ = np.unique(y)
        class_weight_ = np.ones(classes_.shape[0], dtype=np.float64, order='C')
        bias = -1.0
        liblinear.set_verbosity_wrap(1)
        raw_coef_, n_iter_ = liblinear.train_wrap(X, y, self.solver_type, 0, self.tol, bias, self.C,
                                                  class_weight_, self.max_iter, 0, epsilon)

        n_iter_ = max(n_iter_)
        return raw_coef_, n_iter_


if __name__ == '__main__':
    svm = LinearSVM(solver_type=4)

    from sklearn.feature_extraction.text import HashingVectorizer
    import jieba
    from scipy.sparse.base import spmatrix

    def tokenizer(text):
        return jieba.cut(text, cut_all=True)

    text_src = ['aa bb aa', 'bb aa cc', 'cc bb bb', 'cc', 'bb']
    v = HashingVectorizer(tokenizer=tokenizer, n_features=30000, non_negative=True)
    data = v.fit_transform(text_src)
    y = np.asarray([0, 1, 0, 1, 1])
    print isinstance(data, spmatrix)
    svm.fit(data, y)