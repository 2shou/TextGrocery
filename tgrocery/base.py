def read_text_src(text_src, delimiter):
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
        self._compute_accuracy_overall()
        self._compute_accuracy_recall_labels()

    def _compute_accuracy_overall(self):
        l = len(self.true_y)
        self.accuracy_overall = sum([self.true_y[i] == self.predicted_y[i] for i in range(l)]) / float(l)

    def _compute_accuracy_recall_labels(self):
        labels = {}
        for idx, predicted_label in enumerate(self.predicted_y):
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
        for key, val in labels.items():
            try:
                self.accuracy_labels[key] = float(val[0]) / val[1]
            except ZeroDivisionError:
                self.accuracy_labels[key] = float(0)
            try:
                self.recall_labels[key] = float(val[0]) / val[2]
            except ZeroDivisionError:
                self.recall_labels[key] = float(0)

    @staticmethod
    def draw_table(data, row_labels, column_labels):
        row_format = '{:<15}' * (len(column_labels) + 1)
        table_string = '%s\n' % row_format.format('', *column_labels)
        for row_label, row_data in zip(row_labels, data):
            table_string += '%s\n' % row_format.format(row_label, *row_data)
        return table_string

    def show_result(self):
        print(self.draw_table(
            list(zip(
                ['%.2f%%' % (s * 100) for s in list(self.accuracy_labels.values())],
                ['%.2f%%' % (s * 100) for s in list(self.recall_labels.values())]
            )),
            list(self.accuracy_labels.keys()),
            ('accuracy', 'recall')
        ))

    def __str__(self):
        return str(self.accuracy_overall)


class GroceryPredictResult(object):
    def __init__(self, predicted_y=None, dec_values=None, labels=None):
        self.predicted_y = predicted_y
        self.dec_values = dict(list(zip(labels, dec_values)))

    def __str__(self):
        return self.predicted_y
