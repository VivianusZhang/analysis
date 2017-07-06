import ml
from mlData import *


test_set, test_label, validate_set, validate_label = initData().prepare_data()
test = ml.my_ml(test_set, test_label, validate_set, validate_label)

test.train_gcforest()
test.gen_metrics()
test.plot_accuracy()