# -*- coding: utf-8 -*-

# load packages
dyn.load("/home/admin/jingwen.hjw/software/pgsql/lib/libpq.so.5")
library("RPostgreSQL")
library("sqldf")
options(sqldf.RPostgreSQL.user = "admin",
        sqldf.RPostgreSQL.dbname = "kdd-cup-2015")
library("reshape")

########################
### extract features ###
########################

## 1. course related features

# 1.1 DONE 每种Module的数量
category_vec <- as.character(sqldf("select distinct category from object")$"category");
course_vec <- as.character(sqldf("select distinct course_id from object")$"course_id");
result_course_vec <- c()
result_category_vec <- c()
result_count_vec <- c()
for (course_id in course_vec) {
    for (category in category_vec) {
        sql <- paste("select distinct course_id, count(category) from object where category = '",
                     category, "' and course_id = '", course_id, "' group by course_id;", sep = "");
        df <- sqldf(sql);
        result_course_vec <- append(result_course_vec, course_id);
        result_category_vec <- append(result_category_vec, category);
        if (dim(df)[1] == 0) {
            result_count_vec <- append(result_count_vec, 0);
        } else {
            result_count_vec <- append(result_count_vec, df$"count")
        }
    }
}
result <- data.frame(result_course_vec, result_category_vec, result_count_vec);
names(result) <- c("course_id", "category", "count");
feature_category <- cast(result, course_id ~ category, sum);
write.table(feature_category, file = "../data/feature_category_test.csv", row.names = FALSE, quote = FALSE, sep = ",");

# 1.2 DONE 参加人数
result <- sqldf("select course_id, count(distinct username) from log_test group by course_id");
names(result) <- c("course_id", "user_count");
write.table(result, file = "../data/feature_user_count_test.csv", row.names = FALSE, quote = FALSE, sep = ",");

## 2 user features

# 2.1 DONE 历史总共加入过的课程数
result <- sqldf("select username, count(distinct course_id) from log_test group by username");
names(result) <- c("username", "course_count");
write.table(result, file = "../data/feature_history_course_count_test.csv", row.names = FALSE, quote = FALSE, sep = ",");

# 2.2 TODO 历史dropout数量（针对老用户）

# 2.3 TODO 历史pass数量（针对老用户）

## 2 cross featrues

# 2.1 DONE 最后一次浏览时间 - 第一次浏览时间
result <- sqldf("select enrollment_id, username, course_id, to_char(max(time) - min(time), 'DD') from log_test group by enrollment_id, username, course_id");
names(result) <- c("enrollment_id", "username", "course_id", "total_time");
write.table(result, file = "../data/feature_total_time_test.csv", row.names = FALSE, quote = FALSE, sep = ",");

# 2.2 DONE 第一次浏览时间 - 课程开始时间
result <- sqldf("select a.enrollment_id, a.username, a.course_id, to_char(a.min - b.min, 'DD') from
                 (select distinct enrollment_id, username, course_id, min(time) from log_test group by enrollment_id, username, course_id) a,
                 (select distinct course_id, min(time) from log_test group by course_id) b
                 where a.course_id = b.course_id");
names(result) <- c("enrollment_id", "username", "course_id", "left_time");
write.table(result, file = "../data/feature_left_time_test.csv", row.names = FALSE, quote = FALSE, sep = ",");

# 2.3 DONE 课程结束时间 - 最后一次浏览时间
result <- sqldf("select a.enrollment_id, a.username, a.course_id, to_char(b.max - a.max, 'DD') from
                 (select distinct enrollment_id, username, course_id, max(time) from log_test group by enrollment_id, username, course_id) a,
                 (select distinct course_id, max(time) from log_test group by course_id) b
                 where a.course_id = b.course_id");
names(result) <- c("enrollment_id", "username", "course_id", "right_time");
write.table(result, file = "../data/feature_right_time_test.csv", row.names = FALSE, quote = FALSE, sep = ",");

# 2.4 DONE 浏览总次数
result <- sqldf("select enrollment_id, username, course_id, count(*) from log_test group by enrollment_id, username, course_id");
names(result) <- c("enrollment_id", "username", "course_id", "log_count");
write.table(result, file = "../data/feature_log_count_test.csv", row.names = FALSE, quote = FALSE, sep = ",");

# 2.5 DONE 每种event的数量
sql_frame <- sqldf("select enrollment_id, username, course_id, event, count(*) from log_test group by enrollment_id, username, course_id, event");
result <- cast(sql_frame, enrollment_id + username + course_id ~ event, sum)
write.table(result, file = "../data/feature_event_test.csv", row.names = FALSE, quote = FALSE, sep = ",");

# 2.6 TODO 当前同时加入的课程数
#result <- sqldf("");
#names(result) <- c();
#write.table(result, file = "../data/feature_current_course_count_test.csv", row.names = FALSE, quote = FALSE, sep = ",");

#######################
# Disconnect Database #
#######################
#dbDisconnect(con)

