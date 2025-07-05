from enum import StrEnum


class TablesSchema(StrEnum):
    assessments = "assessments"
    courses = "courses"
    studentAssessment = "studentAssessment"
    studentInfo = "studentInfo"
    studentRegistration = "studentRegistration"
    studentVle = "studentVle"
    vle = "vle"


class CoursesSchema(StrEnum):
    code_module = "code_module"
    code_presentation = "code_presentation"
    module_presentation_length = "module_presentation_length"


class StudentInfo(StrEnum):
    code_module = "code_module"
    code_presentation = "code_presentation"
    id_student = "id_student"
    gender = "gender"
    region = "region"
    highest_education = "highest_education"
    imd_band = "imd_band"
    age_band = "age_band"
    num_of_prev_attempts = "num_of_prev_attempts"
    studied_credits = "studied_credits"
    disability = "disability"
    final_result = "final_result"
    # Ordinals
    highest_education_ord = "highest_education_ord"
    age_band_ord = "age_band_ord"
    imd_band_ord = "imd_band_ord"
    final_result_ord = "final_result_ord"


class Assessments(StrEnum):
    code_module = "code_module"
    code_presentation = "code_presentation"
    id_assessment = "id_assessment"
    assessment_type = "assessment_type"
    date = "date"
    weight = "weight"


class Vle(StrEnum):
    id_site = "id_site"
    code_module = "code_module"
    code_presentation = "code_presentation"
    activity_type = "activity_type"
    week_from = "week_from"
    week_to = "week_to"


class StudentAssessment(StrEnum):
    id_student = "id_student"
    id_assessment = "id_assessment"
    date_submitted = "date_submitted"
    is_banked = "is_banked"
    score = "score"


class StudentRegistration(StrEnum):
    code_module = "code_module"
    code_presentation = "code_presentation"
    id_student = "id_student"
    date_registration = "date_registration"
    date_unregistration = "date_unregistration"


class StudentVle(StrEnum):
    id_site = "id_site"
    id_student = "id_student"
    code_module = "code_module"
    code_presentation = "code_presentation"
    date = "date"
    sum_click = "sum_click"
