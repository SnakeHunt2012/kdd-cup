# -*- coding: utf-8 -*-
# PostgreSQL版本

# load packages
library("sqldf")
library("reshape")

# load features
## 1. user feature
### 1.1 feature_history_course_count
feature_history_course_count <- read.csv("../data/feature_history_course_count_train.csv", header = TRUE);

### 1.2 feature_user_event
feature_user_event <- read.csv("../data/feature_user_event_train.csv", header = TRUE);

### 1.3 feature_user_log_count
feature_user_log_count <- read.csv("../data/feature_user_log_count_train.csv", header = TRUE);

## 2. course feature
### 2.1 feature_category
feature_category <- read.csv("../data/feature_category_train.csv", header = TRUE);

### 2.2 feature_user_count
feature_user_count <- read.csv("../data/feature_user_count_train.csv", header = TRUE)

## 3. enrollment feature
### 3.1 feature_enrollment_event
feature_enrollment_event <- read.csv("../data/feature_enrollment_event_train.csv", header = TRUE);

### 3.2 feature_enrollment_log_count
feature_enrollment_log_count <- read.csv("../data/feature_enrollment_log_count_train.csv", header = TRUE);

### 3.3 feature_left_time
feature_left_time <- read.csv("../data/feature_left_time_train.csv", header = TRUE);

### 3.4 feature_right_time
feature_right_time <- read.csv("../data/feature_right_time_train.csv", header = TRUE);

### 3.5 feature_total_time
feature_total_time <- read.csv("../data/feature_total_time_train.csv", header = TRUE);

# aggregate features
## user_features
user_features <- merge(feature_history_course_count, feature_user_event, by = "username", all = TRUE);
user_features <- merge(user_features, feature_user_log_count, all = TRUE);

## course_features
course_features <- merge(feature_category, feature_user_count, by = "course_id", all = TRUE);

## enrollment_features
enrollment_features <- merge(feature_enrollment_event, feature_enrollment_log_count, by = c("enrollment_id", "username", "course_id"), all = TRUE);
enrollment_features <- merge(enrollment_features, feature_left_time, by = c("enrollment_id", "username", "course_id"), all = TRUE);
enrollment_features <- merge(enrollment_features, feature_right_time, by = c("enrollment_id", "username", "course_id"), all = TRUE);
enrollment_features <- merge(enrollment_features, feature_total_time, by = c("enrollment_id", "username", "course_id"), all = TRUE);

## final_features
final_features <- merge(enrollment_features, user_features, by = "username", all = TRUE);
final_features <- merge(final_features, course_features, by = "course_id", all = TRUE);

# load truth_train
truth_train <- read.csv("../data/truth_train.csv", header = FALSE);
names(truth_train) <- c("enrollment_id", "dropout");

# merge feature and target
train_data <- merge(final_features, truth_train, by = "enrollment_id", all = TRUE);
train_data <- train_data[names(train_data) != "username" & names(train_data) != "course_id"];
write.table(train_data, "../data/train_data.csv", row.names = FALSE, quote = FALSE, sep = ",");

