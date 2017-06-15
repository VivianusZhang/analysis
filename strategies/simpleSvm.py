import tushare as ts
import matplotlib as plt
import os

from sklearn import svm
from sklearn.metrics import *

class my_svm:
    def __init__(self):
        pass

    def compute(self):
        data = ts.get_h_data('603999')
        x = data.as_matrix(columns = data.columns[0:5])
        y = []
        for index in range(len(data.index) - 1):
            if data.iloc[index]['close'] < data.iloc[index + 1]['close']:
                y.append(0)
            else:
                y.append(1)
        test_size = int (len(x) * 0.8)

        print '--------start-----'
        clf = svm.SVC(kernel='linear', cache_size= 7000)
        clf.fit(x[0:test_size], y[0:test_size])

        print '------end----------'
        self.labels = y[test_size: len(y)]
        self.predicted = clf.predict_proba(x[test_size : len(x)])

    def gen_metrics(self, highlight_fprs = [0.05]) :
        save_dir = '/Users/vivian/Documents/Programming/analysis/strategies'
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

