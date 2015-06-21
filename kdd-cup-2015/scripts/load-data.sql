/* drop tables */
/*
drop table enrollment_train;
drop table enrollment_test;
drop table log_train;
drop table log_test;
drop table object;
drop table truth_train;
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

create table truth_train (
       enrollment_id	 integer,
       dropout		 boolean
);

/* load tables */
copy enrollment_train
from '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/enrollment_train.csv'
with csv header;

copy enrollment_test
from '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/enrollment_test.csv'
with csv header;

copy log_train
from '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/log_train.csv'
with csv header;

copy log_test
from '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/log_test.csv'
with csv header;

copy object
from '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/object.csv'
with csv header null 'null';

copy truth_train
from '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/truth_train.csv'
with csv;

/* dump tables */
/*
copy enrollment_train
to '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/enrollment_train.sql';

copy enrollment_test
to '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/enrollment_test.sql';

copy log_train
to '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/log_train.sql';

copy log_test
to '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/log_test.sql';

copy object
to '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/object.sql';

copy truth_train
to '/home/admin/jingwen.hjw/learn/kdd-cup-2015/data/truth_train.sql';
*/
