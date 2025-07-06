from enum import StrEnum


class TablesExcelSchema(StrEnum):
    assessments = "Assess Plan"
    courses = "cursos"
    assess_detail = "Assess_detail"
    studentInfo = "StudentInfo"
    studentRegistration = "Registration"
    studentVle = "VLE_clickStream"
    vle = "Vle_modules"


class CoursesExcel(StrEnum):
    code_module = "code_module"
    code_presentation = "code_presentation"
    module_presentation_length = "module_presentation_length"


class StudentInfoExcel(StrEnum):
    code_module = "code_module"
    code_presentation = "code_presentation"
    guid_student_id = "id_student"
    gender = "gender"
    region = "region"
    highest_education = "highest_education"
    imd_band = "imd_band"
    age_band = "age_band"
    num_of_prev_attempts = "num_of_prev_attempts"
    studied_credits = "studied_credits"
    disability = "disability"
    final_result = "final_result"


class AssessmentsExcel(StrEnum):
    code_module = "code_module"
    code_presentation = "code_presentation"
    guid_assess_id = "guid_assess_id"
    assessment_type = "assessment_type"
    date = "date"
    weight = "weight"


class VleExcel(StrEnum):
    guid_site_id = "guid_site_id"
    code_module = "code_module"
    code_presentation = "code_presentation"
    activity_type = "activity_type"
    week_from = "week_from"
    week_to = "week_to"


class AssessmentDetailExcel(StrEnum):
    guid_student_id = "guid_student_id"
    guid_assess_id = "guid_assess_id"
    date_submitted = "date_submitted"
    is_banked = "is_banked"
    score = "score"
    assessment_type = "assessment_type"
    date = "date"
    weight = "weight"
    gender = "gender"
    region = "region"
    highest_education = "highest_education"
    imd_band = "imd_band"
    age_band = "age_band"
    num_of_prev_attempts = "num_of_prev_attempts"
    studied_credits = "studied_credits"
    disability = "disability"
    final_result = "final_result"
    status = "status"
    module = "module"
    presentation = "presentation"
    date_real_days = "date_real_days"
    id_assetcode = "id_assetcode"


class StudentRegistrationExcel(StrEnum):
    guid_student_id = "guid_student_id"
    code_module = "code_module"
    code_presentation = "code_presentation"
    date_registration = "date_registration"
    date_unregistration = "date_unregistration"


class StudentVleExcel(StrEnum):
    guid_site_id = "guid_site_id"
    guid_student_id = "guid_student_id"
    date = "date"
    sum_clics = "sum_clics"
    type_assign = "type_assign"
    week_from = "week_from"
    week_to = "week_to"
    disability = "disability"
    modulo = "modulo"
    week1 = "week1"
    week2 = "week2"
    days = "days"
    presentation = "presentation"
