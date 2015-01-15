def read_text_src(text_src, delimiter='\t'):
    if isinstance(text_src, str):
        with open(text_src, 'r') as f:
            text_src = [line.split(delimiter) for line in f]
    elif not isinstance(text_src, list):
        raise TypeError('text_src should be list or str')
    return text_src


class GroceryTestResult(object):
    def __init__(self, true_y, predicted_y):
        self.true_y = true_y
        self.predicted_y = predicted_y
        self._compute_accuracy()
        self._compute_accuracy_recall()

    def _compute_accuracy(self):
        l = len(self.true_y)
        self.accuracy_overall = sum([self.true_y[i] == self.predicted_y[i] for i in range(l)]) / float(l)

    def _compute_accuracy_recall(self):
        labels = {}
        for idx, r in enumerate(self.predicted_y):
            predicted_label = self.predicted_y[idx]
            true_label = self.true_y[idx]
            if predicted_label not in labels:
                labels[predicted_label] = [0, 0, 0]
            if true_label not in labels:
                labels[true_label] = [0, 0, 0]
            if predicted_label == true_label:
                labels[predicted_label][0] += 1
            labels[predicted_label][1] += 1
            labels[true_label][2] += 1
        self.accuracy_labels = {}
        self.recall_labels = {}
        for key, val in labels.iteritems():
            try:
                self.accuracy_labels[key] = float(val[0]) / val[1]
            except ZeroDivisionError:
                self.accuracy_labels[key] = float(0)
            try:
                self.recall_labels[key] = float(val[0]) / val[2]
            except ZeroDivisionError:
                self.recall_labels[key] = float(0)

    def __str__(self):
        return str(self.accuracy_overall)


class GroceryPredictResult(object):
    def __init__(self, predicted_y=None, dec_values=None, labels=None):
        self.predicted_y = predicted_y
        self.dec_values = dict(zip(labels, dec_values))

    def __str__(self):
        return self.predicted_y