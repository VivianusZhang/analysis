import ml
from mlData import *


test_set, test_label, validate_set, validate_label = initData().prepare_data('600570')
test = ml.my_ml(test_set, test_label, validate_set, validate_label)

test.train_random_forest()
test.gen_metrics()
test.plot_accuracy()