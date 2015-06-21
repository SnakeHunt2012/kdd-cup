select P.projectid, P.students_reached, P.fulfillment_labor_materials, P.total_price_excluding_optional_support, P.total_price_including_optional_support, P.school_latitude, P.school_longitude, char_length(E.essay), char_length(E.short_description), O.is_exciting
from projects P, essays E, outcomes O
where P.projectid = O.projectid and E.projectid = O.projectid
