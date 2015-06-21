import module_io
from sklearn.ensemble import RandomForestClassifier

if __name__=="__main__":

    # look backwared & look forward
    look_backward = 29
    look_forward = 4
    
    # get records from database
    print "getting features from database"
    conn = module_io.db_connect()
    query = module_io.load_sql("../sql/query-features-test.sql")
    records = module_io.db_query(conn, query)

    # load model
    classifier = module_io.load_model("../model/benchmark.pickle")

    # clean features
    features = []
    for record in records:
        vector_feature = list(record[1:])
        for index in range(len(vector_feature)):
            if vector_feature[index] is None:
                vector_feature[index] = 0
        features.append(vector_feature)

    # get features
    range_test = features[look_backward:(-look_forward)]
    features_test = []
    for index in range(look_backward, len(features) - look_forward):
        features_current = []
        features_current.extend(features[index])
        for look in range(1, look_backward + 1):
            features_current.extend(features[index - look])
        for look in range(1, look_forward + 1):
            features_current.extend(features[index + look])
        features_test.append(tuple(features_current))
        
    # test
    predictions_proba = classifier.predict_proba(features_test)[:, 1]
    predictions_proba = list(predictions_proba)

    # combine look_back and look_forward and predictions_proba
    proba_back = [0 for i in range(look_backward)]
    proba_forward = [0 for i in range(look_forward)]
    proba = predictions_proba
    predictions_proba = []
    predictions_proba.extend(proba_back)
    predictions_proba.extend(proba)
    predictions_proba.extend(proba_forward)

    # print submission (to csv)
    with open("../csv/benchmark.csv", 'w') as csv_submission:
        # csv header
        csv_submission.write("projectid,is_exciting\n")
        index = 0
        for index in range(len(records)):
            csv_submission.write("%s,%f\n" % (records[index][0],predictions_proba[index]))
    
    
