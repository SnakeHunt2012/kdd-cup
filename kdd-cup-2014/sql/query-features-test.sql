select S.projectid, P.students_reached, P.fulfillment_labor_materials, P.total_price_excluding_optional_support, P.total_price_including_optional_support, P.school_latitude, P.school_longitude, char_length(E.essay), char_length(E.short_description)
from samplesubmission S, projects P, essays E
where P.projectid = S.projectid and E.projectid = S.projectid
