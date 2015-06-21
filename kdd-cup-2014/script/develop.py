import module_io
import gc
import time
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
#from sklearn.svm import OneClassSVM
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

def get_records():
    '''
    get records from database
    '''
    conn = module_io.db_connect()
    query = module_io.load_sql("../sql/query-features-train.sql")
    records = module_io.db_query(conn, query)
    return records

def clean_records(records):
    '''
    remove records with None value in it
    '''
    index = 0
    while index < len(records):
        flag = 0
        for item in records[index]:
            if item is None:
                flag = 1
                break
        if flag == 1:
            records.pop(index)
            continue
        index = index + 1
    return records

def shuffle_records(records):
    '''
    shuffle records randomly
    '''
    random.shuffle(records)
    return records

def split_records(records):
    '''
    split records for training and validation by 8:2
    '''
    mark = int(float(len(records)) / float(10) * float(8))
    records_train = records[:mark]
    records_validate = records[mark:]
    return records_train, records_validate

def separate_records(records):
    '''
    separate records by positive or negative
    Note: we consider the last item in the tuple
    in the records as the target by default
    '''
    records_positive = []
    records_negative = []
    for record in records:
        if record[-1] == 1:
            records_positive.append(record)
        else:
            records_negative.append(record)
    return records_positive, records_negative

def convert_targets(targets):
    for index in range(len(targets)):
        if targets[index]:
            targets[index] = 1
        else:
            targets[index] = 0
    return targets
    

if __name__=="__main__":

    # look backwared & look forward
    look_backward = 9
    look_forward = 4

    # get records from database
    records = get_records()

    # clean reocrds: remove records with None value in it
    records = clean_records(records)

    # shuffle records randomly
    #records = shuffle_records(records)

    # split records: spliit records to records_train and records_validate
    records_train, records_validate = split_records(records)

    # separate positive and negative records
    #records_train_positive, records_train_negative = separate_records(records_train)
    #records_validate_positive, records_validate_negative = separate_records(records_validate)

    #length_train_positive = len(records_train_positive)
    #length_train_negative = len(records_train_negative)
    #length_validate_positive = len(records_validate_positive)
    #length_validate_negative = len(records_validate_negative)

    # balance positive and negative in training set
    #index_split = 0
    #if length_train_positive < length_train_negative:
    #    index_split = length_train_positive
    #else:
    #    index_split = length_train_negative

    # get final records for training
    #records_train = []
    #records_train.extend(records_train_positive[:index_split])
    #records_train.extend(records_train_negative[:index_split])
    #records_train = shuffle_records(records_train)

    # get features and target for training
    #features_train = [record[1:-1] for record in records_train]
    #target_train = [record[-1] for record in records_train]

    # get features and target for validation
    #features_validate = [record[1:-1] for record in records_validate]
    #target_validate = [record[-1] for record in records_validate]

    # get target and features for training
    range_train = records_train[look_backward:(-look_forward)]
    target_train = [record[-1] for record in range_train]
    features_train = []
    for index in range(look_backward, len(records_train) - look_forward):
        features = []
        features.extend(records_train[index][1:-1])
        for look in range(1, look_backward + 1):
            features.extend(records_train[index - look][1:-1])
        for look in range(1, look_forward + 1):
            features.extend(records_train[index + look][1:-1])
        features_train.append(tuple(features))

    # get target and features for validation
    range_validate = records_validate[look_backward:(-look_forward)]
    target_validate = [record[-1] for record in range_validate]
    features_validate = []
    for index in range(look_backward, len(records_validate) - look_forward):
        features = []
        features.extend(records_validate[index][1:-1])
        for look in range(1, look_backward + 1):
            features.extend(records_validate[index - look][1:-1])
        for look in range(1, look_forward + 1):
            features.extend(records_validate[index + look][1:-1])
        features_validate.append(tuple(features))
    
    # convert target from boolean to int (0 / 1)
    target_train = convert_targets(target_train)
    target_validate = convert_targets(target_validate)

    # development
    parameters_n_estimators = range(5, 1000 + 1, 10)
    parameters_min_samples_split = [10, 15]
    parameters_max_depth = [4, 6, 8, 10, 12, 14, 16, 18]
    parameters = [(n_estimators, min_samples_split, max_depth)
                  for n_estimators in parameters_n_estimators
                  for min_samples_split in parameters_min_samples_split
                  for max_depth in parameters_max_depth]
    #parameters_kernel = ["poly"]
    #parameters_degree = range(1, 100, 1)
    #parameters_gamma = [float(gamma) for gamma in [0]]
    #parameters = [(kernel, degree, gamma)
    #              for kernel in parameters_kernel
    #              for degree in parameters_degree
    #              for gamma in parameters_gamma]

    # print csv header
    with open("../csv/development.csv", 'w') as file_csv:
        file_csv.write("n_estimators,min_samples_split,max_depth,roc_auc_train,roc_auc_validate\n")
        #file_csv.write("kernel,degree,gamma,roc_auc_train,roc_auc_validate,time\n")
        
    for parameter_1, parameter_2, parameter_3 in parameters:
    #for parameter_1, parameter_2, parameter_3 in parameters:   
        # train
        gc.collect()

        # log: print time
        print "new classifier with parameter(%d, %d, %d) at time %s ... " % (parameter_1, parameter_2, parameter_3, time.ctime()),
        #print "new classifier with parameter(%s, %d, %f) at time %s ... " % (parameter_1, parameter_2, parameter_3, time.ctime()),
        classifier = RandomForestClassifier(n_estimators = parameter_1,
                                            min_samples_split = parameter_2,
                                            max_depth = parameter_3,
                                            verbose = 2,
                                            n_jobs = -1,
                                            random_state = 1)
        
        # log: print time
        #print "new classifier with parameter(%s, %d, %f) at time %s ... " % (parameter_1, parameter_2, parameter_3, time.ctime()),
        #
        #classifier = OneClassSVM(kernel = parameter_1,
        #                         degree = parameter_2,
        #                         gamma = parameter_3,
        #                         cache_size = 1024 * 20,
        #                         verbose = True)

        # log: print done
        print "done at %s" % time.ctime()
        

        # log: print time
        print "training classifier at time %s ... " % time.ctime(),
        
        classifier.fit(features_train, target_train)

        # log: print done
        print "done at %s" % time.ctime()
        
        
        # log: print time
        print "predicting training set at time %s ... " % time.ctime(),
        
        # roc_auc on training set
        prediction_train_proba = classifier.predict_proba(features_train)[:, 1]
        #prediction_train = list(classifier.predict(features_train))

        # log: print done
        print "done at %s" % time.ctime()
        
        roc_auc_train = roc_auc_score(target_train, prediction_train_proba)
        #roc_auc_train = roc_auc_score(target_train, prediction_train)

        # log: print time
        print "predicting validation set at time %s ... " % time.ctime(),
        
        # roc_auc on validation set
        prediction_validate_proba = classifier.predict_proba(features_validate)[:, 1]
        #prediction_validate = list(classifier.predict(features_validate))

        # log: print done
        print "done at %s" % time.ctime()
        
        roc_auc_validate = roc_auc_score(target_validate, prediction_validate_proba)
        #roc_auc_validate = roc_auc_score(target_validate, prediction_validate)

        # print csv record
        with open("../csv/development.csv", 'a') as file_csv:
            file_csv.write("%d,%d,%d,%f,%f\n" % (parameter_1, parameter_2, parameter_3, roc_auc_train, roc_auc_validate))
            #file_csv.write("%s,%d,%f,%f,%f,%s\n" % (parameter_1, parameter_2, parameter_3, roc_auc_train, roc_auc_validate, time.ctime()))
