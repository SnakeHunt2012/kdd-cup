create table projects (
       projectid     char(32)	primary	key,
       teacher_acctid		char(32),
       schoolid			char(32),
       school_ncesid		char(32),
       school_latitude		real,
       school_longitude		real,
       school_city		text,
       school_zip		char(2),
       school_metro		char(30),
       school_district		text,
       school_charter		text,
       school_magnet		boolean,
       school_year_round	boolean,
       school_nlns		boolean,
       school_kipp		boolean,
       school_charter_ready_promise	boolean,
       teacher_prefix			char(30),
       teacher_teach_for_america	boolean,
       teacher_ny_teaching_fellow	boolean,
       primary_focus_subject		char(30),
       primary_focus_area		char(30),
       secondary_focus_subject		char(30),
       secondary_focus_area		char(30),
       resource_type			char(30),
       poverty_level			char(30),
       grade_level			char(30),
       fulfillment_labor_materials	real,
       total_price_excluding_optional_support	real,
       total_price_including_optional_support	real,
       students_reached				integer,
       eligible_double_your_impact_match	boolean,
       eligible_almost_home_match		boolean,
       date_posted				date
);

copy projects from '/home/postgres/projects.csv' csv header;

create table essays (
       projectid    char(32)	references projects (projectid),
       teacher_accid	char(32),
       title		text,
       short_description	text,
       need_statement		text,
       essay			text
);

copy essays from '/home/postgres/essays.csv' csv header;

create table donations (
       donationid      char(32)	primary key,
       projectid       char(32)	references projects (projectid),
       donor_acctid    char(32),
       donor_city      text,
       donor_state     char(2),
       donor_zip       char(5),
       is_teacher_acct boolean,
       donation_timestamp	timestamp,
       donation_to_project	real,
       donation_optional_support	real,
       donation_total			real,
       dollar_amount			char(30),
       donation_included_optional_support	boolean,
       payment_method				char(30),
       payment_included_acct_credit		boolean,
       payment_included_campaign_gift_card	boolean,
       payment_included_web_purchased_gift_card	boolean,
       payment_was_promo_matched		boolean,
       via_giving_page				boolean,
       for_honoree				boolean,
       donation_message				text
);

copy donations from '/home/postgres/donations.csv' csv header;

create table resources (
       resourceid      char(32)	primary key,
       projectid       char(32) references projects (projectid),
       vendorid	       smallint,
       vendor_name     text,
       project_resource_type	char(30),
       item_name		text,
       item_number		text,
       item_unit_price		real,
       item_quantity		real
);

copy resources from '/home/postgres/resources.csv' csv header;

create table outcomes (
       projectid      char(32)	references projects (projectid),
       is_exciting    boolean,
       at_least_1_teacher_referred_donor boolean,
       fully_funded			 boolean,
       at_least_1_green_donation	 boolean,
       great_chat			 boolean,
       three_or_more_non_teacher_referred_donors	boolean,
       one_non_teacher_referred_donor_giving_100_plus	boolean,
       donation_from_thoughtful_donor			boolean,
       great_messages_proportion			real,
       teacher_referred_count				real,
       non_teacher_referred_count			real
);

copy outcomes from '/home/postgres/outcomes.csv' csv header;

create table sampleSubmission (
       projectid char(32)     references projects (projectid),
       is_exciting	      boolean
);

copy sampleSubmission from '/home/postgres/sampleSubmission.csv' csv header;