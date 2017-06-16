import os

import matplotlib.pyplot as plt
from  pymongo import MongoClient
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import *

client = MongoClient('localhost', 27017)
db = client['stock']


class my_ml:
    def __init__(self):
        pass

    def prepare_data(self):
        data = list(db.feed.find({'code': {'$ne': '603999'}, 'label': {'$ne': -1}}))
        self.test_set = []
        self.test_label = []
        for value in data:
            self.test_set.append([value['open'], value['close'], value['high'], value['low'], value['volume']])
            self.test_label.append(value['label'])
        data = list(db.feed.find({'code': '603999', 'label': {'$ne': -1}}))
        self.validate_set = []
        self.labels = []
        for value in data:
            self.validate_set.append([value['open'], value['close'], value['high'], value['low'], value['volume']])
            self.labels.append(value['label'])

    def train_svm(self):
        self.prepare_data()
        print '--------start-----'
        clf = svm.SVC(kernel='linear', cache_size=7000, probability=True)
        clf.fit(self.test_set, self.test_label)
        print '------end----------'

        self.predicted = clf.predict_proba(self.validate_set)

    def train_random_forest(self):
        self.prepare_data()
        print len(self.test_set)
        print '--------start-------------'
        clf = RandomForestClassifier(1)
        clf.fit(self.test_set, self.test_label)
        print '---------end--------------'
        self.predicted = clf.predict_proba(self.validate_set)

    def gen_metrics(self, highlight_fprs=[0.05]):
        save_dir = '/home/vivianzhang/Documents/analysis/'
        roc_file = os.path.join(save_dir, 'ROC.png')
        fpr_tpr_file = os.path.join(save_dir, 'fpr_tpr.png')
        fpr_accuracy_file = os.path.join(save_dir, 'accuracy.png')
        fpr, tpr, threshold = roc_curve(self.labels, self.predicted[:, 1])
        roc_auc = auc(fpr, tpr)

        highlight_tprs = [0] * len(highlight_fprs)
        highlight_threshs = [0] * len(highlight_fprs)
        roc_fig = plt.figure(100)
        roc_ax = roc_fig.add_subplot(111)
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')

        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC')
        plt.legend(loc='lower right')
        for i in range(len(highlight_fprs)):
            highlight_tprs[i] = self._get_y_value_by_x_value(fpr, tpr, highlight_fprs[i])
            plt.plot(highlight_fprs[i], highlight_tprs[i], 'ro', color='blue')
            roc_ax.annotate('({:2.4f}, {:2.4f})'.format(highlight_fprs[i], highlight_tprs[i]),
                            xy=(highlight_fprs[i], highlight_tprs[i]))
        plt.savefig(roc_file)

        fts_fig = plt.figure(101)
        fts_ax = fts_fig.add_subplot(111)
        plt.plot(threshold, fpr, color='cyan', lw=2, label='False Posivite Rate')
        plt.plot(threshold, tpr, color='magenta', lw=2, label='True Posivite Rate')
        for i in range(len(highlight_fprs)):
            highlight_threshs[i] = self._get_y_value_by_x_value(fpr, threshold, highlight_fprs[i])
            plt.plot(highlight_threshs[i], highlight_tprs[i], 'ro')
            plt.plot(highlight_threshs[i], highlight_fprs[i], 'ro')
            fts_ax.annotate('({:2.4f}, {:2.4f})'.format(highlight_threshs[i], highlight_tprs[i]),
                            xy=(highlight_threshs[i], highlight_tprs[i]), xytext=(0.7, highlight_tprs[i]),
                            textcoords='axes fraction')
            fts_ax.annotate('({:2.4f}, {:2.4f})'.format(highlight_threshs[i], highlight_fprs[i]),
                            xy=(highlight_threshs[i], highlight_fprs[i]), xytext=(0.7, highlight_fprs[i]),
                            textcoords='axes fraction')
        plt.xlabel('Threshold')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.title('FPR, TPR')
        plt.legend(loc='lower left')
        plt.savefig(fpr_tpr_file)

    def compute_return(self):
        timeseries_prediccted = reversed(self.predicted)
        timeseries_price = reversed(self.validate_set)

        for i in range(len(timeseries_prediccted)):
            if timeseries_prediccted[i][1] == 1:
                pass

    @staticmethod
    def _get_y_value_by_x_value(x_values, y_values, x):
        # x_values = np.sort(x_values)
        # y_values = np.sort(y_values)
        for i in range(x_values.shape[0] - 1):
            if x_values[i] == x:
                return y_values[i]
            if (x_values[i] < x < x_values[i + 1]) or (x_values[i] > x > x_values[i + 1]):
                # linear interpolation
                return (
                           (y_values[i + 1] - y_values[i]) * x - x_values[i] * y_values[i + 1] + x_values[i + 1] *
                           y_values[i]) / (x_values[i + 1] - x_values[i])
