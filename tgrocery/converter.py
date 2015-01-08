"""
TextGrocery is a simple short-text classification tool based on LibShortText.
"""

from collections import defaultdict

import jieba

__all__ = ['GroceryTextConverter']


class GroceryTextPreProcessor(object):
    def __init__(self):
        self.tok2idx = {}

    @staticmethod
    def _default_tokenize(text):
        return jieba.cut(text, cut_all=True)

    def preprocess(self, text):
        tokens = self._default_tokenize(text)
        ret = []
        for idx, tok in enumerate(tokens):
            if tok not in self.tok2idx:
                self.tok2idx[tok] = len(self.tok2idx)
            ret.append(self.tok2idx[tok])
        return ret


class GroceryFeatureGenerator(object):
    def __init__(self):
        self.ngram2fidx = {}

    def unigram(self, tokens):
        feat = defaultdict(int)
        NG = self.ngram2fidx
        for x in tokens:
            if (x,) not in NG:
                NG[x,] = len(NG)
            feat[NG[x,]] += 1
        return feat

    def bigram(self, tokens):
        feat = self.unigram(tokens)
        NG = self.ngram2fidx
        for x, y in zip(tokens[:-1], tokens[1:]):
            if (x, y) not in NG:
                NG[x, y] = len(NG)
            feat[NG[x, y]] += 1
        return feat


class GroceryClassMapping(object):
    def __init__(self):
        self.class2idx = {}

    def to_idx(self, class_name):
        if class_name in self.class2idx:
            return self.class2idx[class_name]

        m = len(self.class2idx)
        self.class2idx[class_name] = m
        return m


class GroceryTextConverter(object):
    def __init__(self):
        self.text_prep = GroceryTextPreProcessor()
        self.feat_gen = GroceryFeatureGenerator()
        self.class_map = GroceryClassMapping()

    def transfer_svm(self, text, class_name=None):
        feat = self.feat_gen.bigram(self.text_prep.preprocess(text))
        return feat, self.class_map.to_idx(class_name)

    def convert_text(self, text_src, output=None):
        if not output:
            output = '%s.svm' % text_src
        with open(output, 'w') as w:
            with open(text_src, 'r') as f:
                for line in f:
                    try:
                        label, text = line.split('\t', 1)
                    except ValueError:
                        continue
                    feat, label = self.transfer_svm(text, label)
                    w.write('%s %s\n' % (label, ''.join(' {0}:{1}'.format(f, feat[f]) for f in sorted(feat))))