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
        raw_coef_, n_iter_ = liblinear.train_wrap(X, y, self.solver_type, 1, self.tol, bias, self.C,
                                                  class_weight_, self.max_iter, 0, epsilon)

        n_iter_ = max(n_iter_)
        return raw_coef_, n_iter_


class FakeSparse(object):
    def __init__(self):
        self.data = None
        self.indices = None
        self.indptr = None
        self.shape = None


if __name__ == '__main__':
    svm = LinearSVM(solver_type=4)

    from sklearn.feature_extraction.text import CountVectorizer
    import jieba
    from scipy.sparse.base import spmatrix

    def tokenizer(text):
        return jieba.cut(text, cut_all=True)

    train_words = ['aa bb aa ee kk ff', 'bb ss aa cc', 'cc bb bb', 'cc', 'bb dd', 'll gg xx']
    # v = CountVectorizer(tokenizer=tokenizer)
    # train_data = v.fit_transform(train_words)
    train_data = FakeSparse()
    train_data.data = np.asarray([2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=np.int64)
    train_data.indices = np.asarray([0, 1, 0, 1, 2, 4, 1, 2, 3, 4, 0, 0, 5, 0, 5, 1, 5], dtype=np.int32)
    train_data.indptr = np.asarray([0, 2, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17], dtype=np.int32)
    train_data.shape = (6, 11)
    # print train_data.data.dtype
    # print train_data.indices.shape
    # print train_data.indices.dtype
    # print train_data.indptr.shape
    # print train_data.indptr.dtype
    # print train_data.shape
    y = [0, 1, 0, 1, 1, 0]
    print isinstance(train_data, spmatrix)
    svm.fit(train_data, y)