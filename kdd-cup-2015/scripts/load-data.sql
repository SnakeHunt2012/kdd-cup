/* drop tables */
/*
drop table enrollment_train;
drop table enrollment_test;
drop table log_train;
drop table log_test;
drop table object;
drop table date;
drop table truth_train;
drop table rf_meta;
drop table gb_meta;
drop table svm_meta;
*/

/* create tables */
create table enrollment_train (
       enrollment_id	      integer,
       username		      char(32),
       course_id	      char(32)
);

create table enrollment_test (
       enrollment_id	      integer,
       username		      char(32),
       course_id	      char(32)
);

create table log_train (
       enrollment_id	      integer,
       username		      char(32),
       course_id	      char(32),
       time		      timestamp without time zone,
       source		      varchar(7),
       event		      varchar(10),
       object		      char(32)
);

create table log_test (
       enrollment_id	      integer,
       username		      char(32),
       course_id	      char(32),
       time		      timestamp without time zone,
       source		      varchar(7),
       event		      varchar(10),
       object		      char(32)
);

create table object (
       course_id    char(32),
       module_id    char(32),
       category	    varchar(17),
       children	    text,
       start	    timestamp without time zone
);

create table date (
       course_id  char(32),
       date_from  timestamp without time zone,
       date_to	  timestamp without time zone
);

create table truth_train (
       enrollment_id	 integer,
       dropout		 boolean
);

create table rf_meta (
       model			varchar,

       timestamp		timestamp,
       pid			int4,
       tid			int8,
       
       warm_start		boolean,
       oob_score		boolean,
       n_jobs			integer,
       max_leaf_nodes		integer,
       bootstrap		boolean,
       min_samples_leaf		integer,
       n_estimators		integer,
       min_samples_split	integer,
       min_weight_fraction_leaf	float8,
       criterion		varchar,
       random_state		integer,
       max_features		varchar,
       max_depth		integer,
       class_weight		varchar,
       
       acc_train		float8,
       acc_validate		float8,
       logloss_train		float8,
       logloss_validate		float8,
       auc_train		float8,
       auc_validate		float8,

       target			varchar,
       filename			varchar,

       primary key(model, timestamp, pid, tid)
);

create table gb_meta (
       model			varchar,
       
       timestamp		timestamp,
       pid			int4,
       tid			int8,
       
       loss			varchar,
       subsample		float8,
       max_leaf_nodes		integer,
       learning_rate		float8,
       min_samples_leaf		integer,
       n_estimators		integer,
       min_samples_split	integer,
       init			varchar,
       min_weight_fraction_leaf	float8,
       max_features		varchar,
       max_depth		integer,

       acc_train		float8,
       acc_validate		float8,
       logloss_train		float8,
       logloss_validate		float8,
       auc_train		float8,
       auc_validate		float8,
       
       target			varchar,
       filename			varchar,
       
       primary key(model, timestamp, pid, tid)
);

create table svm_meta (
       model			varchar,
       
       timestamp		timestamp,
       pid			int4,
       tid			int8,
       
       kernel			varchar,
       C			float8,
       probability		boolean,
       degree			integer,
       scaler			varchar,
       shrinking		boolean,
       max_iter			integer,
       random_state		integer,
       tol			float8,
       cache_size		integer,
       coef0			float8,
       gamma			float8,
       class_weight		varchar,

       acc_train		float8,
       acc_validate		float8,
       logloss_train		float8,
       logloss_validate		float8,
       auc_train		float8,
       auc_validate		float8,
       
       target			varchar,
       filename			varchar,
       
       primary key(model, timestamp, pid, tid)
);

/* load tables */
copy enrollment_train
from '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/enrollment_train.csv'
with csv header;

copy enrollment_test
from '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/enrollment_test.csv'
with csv header;

copy log_train
from '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/log_train.csv'
with csv header;

copy log_test
from '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/log_test.csv'
with csv header;

copy date
from '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/date.csv'
with csv header null 'null';

copy object
from '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/object.csv'
with csv header null 'null';

copy truth_train
from '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/truth_train.csv'
with csv;

/* dump tables */
/*
copy enrollment_train
to '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/enrollment_train.sql';

copy enrollment_test
to '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/enrollment_test.sql';

copy log_train
to '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/log_train.sql';

copy log_test
to '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/log_test.sql';

copy date
to '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/date.sql';

copy object
to '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/object.sql';

copy truth_train
to '/apsarapangu/disk5/jingwen.hjw/learn/kdd-cup/kdd-cup-2015/data/truth_train.sql';
*/
