import module_io
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

if __name__=="__main__":

    # look forward and look backward
    look_forward = 29
    look_backward = 4
    
    # get records from database
    print "getting features from database"
    conn = module_io.db_connect()
    query = module_io.load_sql("../sql/query-features-train.sql")
    records = module_io.db_query(conn, query)

    # clean records: remove None records
    index_record = 0
    while index_record < len(records):
        # judge whether have value None in this record
        flag_none = 0
        for item in records[index_record]:
            if item is None:
                flag_none = 1
        # if there is a None in this record: remove this record
        if flag_none == 1:
            records.pop(index_record)
            continue
        index_record = index_record + 1

    # shuffle records
    #random.shuffle(records)

    # split for training set and cross-validation set
    mark_split = int(len(records) / 10 * 8)
    data_set_train = records[:mark_split]
    data_set_validate = records[mark_split:]

    # list of positive in data_set_train
    #list_positive_train = []

    # list of negative in data_set_train
    #list_negative_train = []

    # fill list_positive_train and list_negative_train
    #for record in data_set_train:
    #    if record[-1] == 1:
    #        list_positive_train.append(record)
    #    else:
    #        list_negative_train.append(record)

    # length of list_positive_train
    #length_positive_train = len(list_positive_train)

    # length of list_negative_train
    #length_negative_train = len(list_negative_train)

    # the minimum length of list_positive_train or list_negative_train
    #length_min_train = 0
    #if length_positive_train < length_negative_train:
    #    length_min_train = length_positive_train
    #else:
    #    length_min_train = length_negative_train

    # get the final list_train for training
    #list_train = []
    #list_train.extend(list_positive_train[:length_min_train])
    #list_train.extend(list_negative_train[:length_min_train])

    # shuffled list of positive and negative in data_set_train
    #random.shuffle(list_train)

    # get features and target for training
    #features_train = [sample[1:-1] for sample in list_train]
    #target_train = [sample[-1] for sample in list_train]
    #for index in range(len(target_train)):
    #    if target_train[index]:
    #        target_train[index] = 1
    #    else:
    #        target_train[index] = 0
            
    # length of list_positive_validate
    #length_positive_validate = len(list_positive_validate)

    # length of list_negative_validate
    #length_negative_validate = len(list_negative_validate)
    
    # get features and target for validation
    #features_validate = [record[1:-1] for record in data_set_validate]
    #target_validate = [record[-1] for record in data_set_validate]
    #for index in range(len(target_validate)):
    #    if target_validate[index]:
    #        target_validate[index] = 1
    #    else:
    #        target_validate[index] = 0

    # list of positive in data_set_validate
    #list_positive_validate = []

    # list of negative in data_set_validate
    #list_negative_validate = []

    # fill list_positive_validate and list_negative_validate
    #for record in data_set_validate:
    #    if record[-1] == 1:
    #        list_positive_validate.append(record)
    #    else:
    #        list_negative_validate.append(record)

    # get target and features for training
    range_train = data_set_train[look_backward:(-look_forward)]
    target_train = [record[-1] for record in range_train]
    features_train = []
    for index in range(look_backward, len(data_set_train) - look_forward):
        features = []
        features.extend(data_set_train[index][1:-1])
        for look in range(1, look_backward + 1):
            features.extend(data_set_train[index - look][1:-1])
        for look in range(1, look_forward + 1):
            features.extend(data_set_train[index + look][1:-1])
        features_train.append(tuple(features))

    # get target and features for validation
    range_validate = data_set_validate[look_backward:(-look_forward)]
    target_validate = [record[-1] for record in range_validate]
    features_validate = []
    for index in range(look_backward, len(data_set_validate) - look_forward):
        features = []
        features.extend(data_set_validate[index][1:-1])
        for look in range(1, look_backward + 1):
            features.extend(data_set_validate[index - look][1:-1])
        for look in range(1, look_forward + 1):
            features.extend(data_set_validate[index + look][1:-1])
        features_validate.append(tuple(features))

    # convert from boolean to integer
    for index in range(len(target_train)):
        if target_train[index]:
            target_train[index] = 1
        else:
            target_train[index] = 0

    # convert from boolean to integer
    for index in range(len(target_validate)):
        if target_validate[index]:
            target_validate[index] = 1
        else:
            target_validate[index] = 0

    # train
    print "training the classifier"
    classifier = RandomForestClassifier(n_estimators=500,
                                        verbose=2,
                                        n_jobs=-1,
                                        min_samples_split=10,
                                        random_state=1)
    classifier.fit(features_train, target_train)

    # validate
    prediction_validate_proba = classifier.predict_proba(features_validate)[:, 1]
    prediction_validate_proba = list(prediction_validate_proba)
    prediction_validate = []
    for validate_proba in prediction_validate_proba:
        if validate_proba > 0.5:
            prediction_validate.append(1)
        else:
            prediction_validate.append(0)

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for index in range(len(target_validate)):
        if prediction_validate[index] == 1:
            if target_validate[index] == 1:
                true_positive = true_positive + 1
                #print "true_positive:\tpredict-%d\tactual-%d" % (prediction_validate[index], target_validate[index])
            else:
                false_positive = false_positive + 1
                #print "false_positive:\tpredict-%d\tactual-%d" % (prediction_validate[index], target_validate[index])
        else:
            if target_validate[index] == 0:
                true_negative = true_negative + 1
                #print "true_negative:\tpredict-%d\tactual-%d" % (prediction_validate[index], target_validate[index])
            else:
                false_negative = false_negative + 1
                #print "false_negative:\tpredict-%d\tactual-%d" % (prediction_validate[index], target_validate[index])
    
    # print roc (to csv)
    fpr, tpr, thresholds = roc_curve(target_validate,
                                     prediction_validate_proba,
                                     pos_label = 1)
    with open("../csv/roc.csv", 'w') as file_csv:
        for index in range(len(fpr)):
            file_csv.write("%d,%d,%d\n" % (fpr[index], tpr[index], thresholds[index]))
    
    # print validation result (to stdio)
    print
    #print "positive sample amount (total) in training set:\t%d" % length_positive_train
    #print "negative sample amount (total) in training set:\t%d" % length_negative_train
    #print "positive sample amount (used) in training set:\t%d" % length_min_train
    #print "negative sample amount (used) in training set:\t%d" % length_min_train
    print
    #print "positive sample amount (total) in validation set:\t%d" % length_positive_validate
    #print "positive sample amount (total) in validation set:\t%d" % length_negative_validate
    #print "positive sample amount (used) in validation set:\t%d" % length_positive_validate
    #print "negative sample amount (used) in validation set:\t%d" % length_negative_validate
    print
    print "true-positive:", true_positive
    print "true-negative", true_negative
    print "false-positive:", false_positive
    print "false-negative", false_negative
    print

    roc_auc = roc_auc_score(target_validate, prediction_validate_proba)
    print "AUC:", roc_auc

    #precision = float(true_positive) / (float(true_positive) + float(false_positive))
    #recall = float(true_positive) / (float(true_positive) + float(false_negative))
    #fscore = 2 * (precision * recall) / (precision + recall)
    
    #print "Precision:", precision
    #Print "Recall:", Recall
    #Print "F-Score:", fscore
    
    # save model
    print "saving the classifier"
    module_io.save_model(classifier)

