# -*- coding: utf-8 -*-
# PostgreSQL版本

# load packages
#dyn.load("/home/admin/jingwen.hjw/software/pgsql/lib/libpq.so.5")
#library("RPostgreSQL")
library("sqldf")
#options(sqldf.RPostgreSQL.user = "admin",
#        sqldf.RPostgreSQL.dbname = "kdd-cup-2015")
library("reshape")

# load features
## 1. user feature
### 1. feature_history_course_count
feature_history_course_count <- read.csv("../data/feature_history_course_count.csv", header = TRUE);

## 2. course feature
### 2.1 feature_category
feature_category <- read.csv("../data/feature_category.csv", header = TRUE);

### 2.2 feature_user_count
feature_user_count <- read.csv("../data/feature_user_count.csv", header = TRUE)

## 3. enrollment feature
### 3.1 feature_event
feature_event <- read.csv("../data/feature_event.csv", header = TRUE);

### 3.2 feature_log_count
feature_log_count <- read.csv("../data/feature_log_count.csv", header = TRUE);

### 3.3 feature_left_time
feature_left_time <- read.csv("../data/feature_left_time.csv", header = TRUE);

### 3.4 feature_right_time
feature_right_time <- read.csv("../data/feature_right_time.csv", header = TRUE);

### 3.5 feature_total_time
feature_total_time <- read.csv("../data/feature_total_time.csv", header = TRUE);

# aggregate features
## user_features
#user_features <- sqldf("select * from feature_history_course_count");
#user_features <- user_features[!duplicated(names(user_features))]; # remove identical columns
user_features <- feature_history_course_count;

## course_features
#course_features <- sqldf("select * from feature_category, feature_user_count where feature_category.course_id = feature_user_count.course_id");
#course_features <- course_features[!duplicated(names(course_features))]; # remove identical columns
course_features <- merge(feature_category, feature_user_count, by = "course_id", all = TRUE);

## enrollment_features
#enrollment_features <- sqldf("select * from feature_event, feature_log_count, feature_left_time, feature_right_time, feature_total_time
#                              where feature_event.enrollment_id = feature_log_count.enrollment_id and
#                                    feature_log_count.enrollment_id = feature_left_time.enrollment_id and
#                                    feature_left_time.enrollment_id = feature_right_time.enrollment_id and
#                                    feature_right_time.enrollment_id = feature_total_time.enrollment_id");
#enrollment_features <- enrollment_features[!duplicated(names(enrollment_features))]; # remove identical columns
enrollment_features <- merge(feature_event, feature_log_count, by = c("enrollment_id", "username", "course_id"), all = TRUE);
enrollment_features <- merge(enrollment_features, feature_left_time, by = c("enrollment_id", "username", "course_id"), all = TRUE);
enrollment_features <- merge(enrollment_features, feature_right_time, by = c("enrollment_id", "username", "course_id"), all = TRUE);
enrollment_features <- merge(enrollment_features, feature_total_time, by = c("enrollment_id", "username", "course_id"), all = TRUE);

## final_features
#final_features <- sqldf("select * from enrollment_features, user_features, course_features
#                         where enrollment_features.username = user_features.username and
#                               enrollment_features.course_id = course_features.course_id");
#final_features <- final_features[(names(final_features) != "username" & names(final_features) != "course_id")];
final_features <- merge(enrollment_features, user_features, by = "username", all = TRUE);
final_features <- merge(final_features, course_features, by = "course_id", all = TRUE);

# load truth_train
truth_train <- read.csv("../data/truth_train.csv", header = FALSE);
names(truth_train) <- c("enrollment_id", "dropout");

# merge feature and target
#train_data <- sqldf("select * from final_features, truth_train
#                     where truth_train.enrollment_id = final_features.enrollment_id");
#train_data <- train_data[!(duplicated(names(train_data)) & names(train_data) == "enrollment_id")];
train_data <- merge(final_features, truth_train, by = "enrollment_id", all = TRUE);
train_data <- train_data[names(train_data) != "username" & names(train_data) != "course_id"];
write.table(train_data, "../data/train_data.csv", row.names = FALSE, quote = FALSE, sep = ",");

