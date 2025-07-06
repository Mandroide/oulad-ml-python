import pathlib
import uuid

import pandas as pd

from oulad_etl.etl.csv_models import (
    AssessmentsCsv,
    CoursesCsv,
    StudentAssessmentCsv,
    StudentInfoCsv,
    StudentRegistrationCsv,
    StudentVleCsv,
    TablesCsvSchema,
    VleCsv,
)
from oulad_etl.etl.excel_models import (
    AssessmentDetailExcel,
    AssessmentsExcel,
    StudentInfoExcel,
    StudentRegistrationExcel,
    StudentVleExcel,
    TablesExcelSchema,
    VleExcel,
)
from oulad_etl.log import log


def __clean_common_columns_csv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia columnas comunes como 'code_module', 'code_presentation', 'id_student'
    convirtiéndolas a strings y eliminando espacios extra.
    """

    for col in [
        CoursesCsv.code_module,
        CoursesCsv.code_presentation,
        StudentInfoCsv.id_student,
        AssessmentsCsv.id_assessment,
        VleCsv.id_site,
    ]:
        if col in df.columns:
            # Convertir a string primero para manejar posibles nulos o tipos mixtos antes de strip
            df[col] = df[col].astype(str).str.strip()
    return df


def add_guid_to_csv(
    dataframes: dict[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:  # Assessments
    df_assessments = dataframes[TablesCsvSchema.assessments]
    df_assessments[AssessmentsExcel.guid_assess_id] = [
        uuid.uuid4() for _ in range(len(df_assessments))
    ]

    # studentAssessment
    df_student_assessment = dataframes[TablesCsvSchema.studentAssessment]
    df_student_assessment[AssessmentsExcel.guid_assess_id] = [
        uuid.uuid4() for _ in range(len(df_student_assessment))
    ]
    df_student_assessment[StudentRegistrationExcel.guid_student_id] = [
        uuid.uuid4() for _ in range(len(df_student_assessment))
    ]

    # Student Registration
    df_student_registration = dataframes[TablesCsvSchema.studentRegistration]
    df_student_registration[StudentRegistrationExcel.guid_student_id] = [
        uuid.uuid4() for _ in range(len(df_student_registration))
    ]

    # Student Vle
    df_student_vle = dataframes[TablesCsvSchema.studentVle]
    df_student_vle[StudentVleExcel.guid_student_id] = [
        uuid.uuid4() for _ in range(len(df_student_vle))
    ]
    df_student_vle[StudentVleExcel.guid_site_id] = [
        uuid.uuid4() for _ in range(len(df_student_vle))
    ]

    # Student Info
    df_student_info = dataframes[TablesCsvSchema.studentInfo]
    df_student_info[StudentInfoExcel.guid_student_id] = [
        uuid.uuid4() for _ in range(len(df_student_info))
    ]

    # vle
    df_vle = dataframes[TablesCsvSchema.vle]
    df_vle[VleExcel.guid_site_id] = [uuid.uuid4() for _ in range(len(df_vle))]

    return dataframes


def remove_id_to_csv(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    df_assessments = dataframes[TablesCsvSchema.assessments]
    df_assessments.drop(columns=[AssessmentsCsv.id_assessment], inplace=True)

    # studentAssessment
    df_student_assessment = dataframes[TablesCsvSchema.studentAssessment]
    df_student_assessment.drop(
        columns=[StudentAssessmentCsv.id_assessment], inplace=True
    )
    df_student_assessment.drop(columns=[StudentAssessmentCsv.id_student], inplace=True)

    # Student Registration
    df_student_registration = dataframes[TablesCsvSchema.studentRegistration]
    df_student_registration.drop(
        columns=[StudentRegistrationCsv.id_student], inplace=True
    )

    # Student Vle
    df_student_vle = dataframes[TablesCsvSchema.studentVle]
    df_student_vle.drop(columns=[StudentVleCsv.id_student], inplace=True)
    df_student_vle.drop(columns=[StudentVleCsv.id_site], inplace=True)

    # Student Info
    df_student_info = dataframes[TablesCsvSchema.studentInfo]
    df_student_info.drop(columns=[StudentInfoCsv.id_student], inplace=True)

    # vle
    df_vle = dataframes[TablesCsvSchema.vle]
    df_vle.drop(columns=[VleCsv.id_site], inplace=True)

    return dataframes


def clean_csv(
    dataframes: dict[str, pd.DataFrame], target: pathlib.Path
) -> dict[str, pd.DataFrame]:
    log.debug("Limpiando 'assessments'...")
    df_assessments = dataframes[TablesCsvSchema.assessments]
    if AssessmentsCsv.date in df_assessments.columns:
        df_assessments[AssessmentsCsv.date] = pd.to_numeric(
            df_assessments[AssessmentsCsv.date], errors="coerce"
        )
        df_assessments[AssessmentsCsv.weight] = pd.to_numeric(
            df_assessments[AssessmentsCsv.weight], errors="coerce"
        )
        df_assessments.dropna(
            subset=[AssessmentsCsv.date, AssessmentsCsv.weight], inplace=True
        )
        df_assessments[AssessmentsCsv.weight] = df_assessments[
            AssessmentsCsv.weight
        ].fillna(df_assessments[AssessmentsCsv.weight].mean())
    df_assessments = __clean_common_columns_csv(df_assessments)
    dataframes[TablesCsvSchema.assessments] = (
        df_assessments  # Actualizar el DataFrame limpio en el diccionario
    )

    log.debug(f"  - 'assessments' limpio. Shape: {df_assessments.shape}")

    # DataFrame: courses
    log.debug("Limpiando 'courses'...")
    df_courses = dataframes[TablesCsvSchema.courses]
    df_courses = __clean_common_columns_csv(df_courses)
    dataframes[TablesCsvSchema.courses] = df_courses
    log.debug(f"  - 'courses' limpio. Shape: {df_courses.shape}")

    # DataFrame: studentAssessment
    log.debug("Limpiando 'studentAssessment'...")
    df_student_assessment = dataframes[TablesCsvSchema.studentAssessment]
    df_student_assessment[StudentAssessmentCsv.score] = pd.to_numeric(
        df_student_assessment[StudentAssessmentCsv.score], errors="coerce"
    )
    df_student_assessment[StudentAssessmentCsv.score] = df_student_assessment[
        StudentAssessmentCsv.score
    ].fillna(0)
    df_student_assessment[StudentAssessmentCsv.date_submitted] = pd.to_numeric(
        df_student_assessment[StudentAssessmentCsv.date_submitted], errors="coerce"
    )
    df_student_assessment.dropna(
        subset=[StudentAssessmentCsv.date_submitted], inplace=True
    )
    df_student_assessment = __clean_common_columns_csv(df_student_assessment)
    dataframes[TablesCsvSchema.studentAssessment] = df_student_assessment
    log.debug(f"  - 'studentAssessment' limpio. Shape: {df_student_assessment.shape}")

    # DataFrame: studentInfo
    log.debug("Limpiando 'studentInfo'...")
    df_student_info = dataframes[TablesCsvSchema.studentInfo]
    for field in [
        StudentInfoCsv.gender,
        StudentInfoCsv.region,
        StudentInfoCsv.highest_education,
        StudentInfoCsv.imd_band,
        StudentInfoCsv.age_band,
        StudentInfoCsv.disability,
        StudentInfoCsv.final_result,
    ]:
        df_student_info[field] = df_student_info[field].fillna(
            df_student_info[field].mode()[0]
        )

    df_student_info[StudentInfoCsv.imd_band] = df_student_info[
        StudentInfoCsv.imd_band
    ].replace("10-20", "10-20%")
    df_student_info[StudentInfoCsv.num_of_prev_attempts] = df_student_info[
        StudentInfoCsv.num_of_prev_attempts
    ].fillna(df_student_info[StudentInfoCsv.num_of_prev_attempts].median())
    df_student_info[StudentInfoCsv.studied_credits] = df_student_info[
        StudentInfoCsv.studied_credits
    ].fillna(df_student_info[StudentInfoCsv.studied_credits].median())

    df_student_info = __clean_common_columns_csv(df_student_info)
    dataframes[TablesCsvSchema.studentInfo] = df_student_info
    log.debug(f"  - 'studentInfo' limpio. Shape: {df_student_info.shape}")

    # DataFrame: studentRegistration
    log.debug("Limpiando 'studentRegistration'...")
    df_student_registration = dataframes[TablesCsvSchema.studentRegistration]
    df_student_registration[StudentRegistrationCsv.date_registration] = pd.to_numeric(
        df_student_registration[StudentRegistrationCsv.date_registration],
        errors="coerce",
    )
    df_student_registration[StudentRegistrationCsv.date_unregistration] = pd.to_numeric(
        df_student_registration[StudentRegistrationCsv.date_unregistration],
        errors="coerce",
    )

    df_student_registration[StudentRegistrationCsv.date_unregistration] = (
        df_student_registration[StudentRegistrationCsv.date_unregistration].fillna(-1)
    )
    df_student_registration.dropna(
        subset=[StudentRegistrationCsv.date_registration], inplace=True
    )
    df_student_registration = __clean_common_columns_csv(df_student_registration)
    dataframes[TablesCsvSchema.studentRegistration] = df_student_registration
    log.debug(
        f"  - 'studentRegistration' limpio. Shape: {df_student_registration.shape}"
    )

    # DataFrame: studentVle
    log.debug("Limpiando 'studentVle'...")
    df_student_vle = dataframes[TablesCsvSchema.studentVle]
    df_student_vle[StudentVleCsv.date] = pd.to_numeric(
        df_student_vle[StudentVleCsv.date], errors="coerce"
    )
    df_student_vle[StudentVleCsv.sum_click] = pd.to_numeric(
        df_student_vle[StudentVleCsv.sum_click], errors="coerce"
    )
    df_student_vle.dropna(
        subset=[StudentVleCsv.date, StudentVleCsv.sum_click], inplace=True
    )
    df_student_vle = __clean_common_columns_csv(df_student_vle)
    dataframes[TablesCsvSchema.studentVle] = df_student_vle
    log.debug(f"  - 'studentVle' limpio. Shape: {df_student_vle.shape}")

    # DataFrame: vle
    log.debug("Limpiando 'vle'...")
    df_vle = dataframes[TablesCsvSchema.vle]
    df_vle[VleCsv.activity_type] = df_vle[VleCsv.activity_type].fillna(
        df_vle[VleCsv.activity_type].mode()[0]
    )
    df_vle[VleCsv.week_from] = pd.to_numeric(df_vle[VleCsv.week_from], errors="coerce")
    df_vle[VleCsv.week_to] = pd.to_numeric(df_vle[VleCsv.week_to], errors="coerce")
    df_vle[VleCsv.week_from] = df_vle[VleCsv.week_from].fillna(-1)
    df_vle[VleCsv.week_to] = df_vle[VleCsv.week_to].fillna(-1)
    df_vle = __clean_common_columns_csv(df_vle)
    dataframes[TablesCsvSchema.vle] = df_vle
    log.debug(f"  - 'vle' limpio. Shape: {df_vle.shape}")

    log.info("Proceso de limpieza de datos completado. ✅")

    # --- 4. Guardar los DataFrames limpios en la nueva carpeta ---
    log.info(f"Guardando los datasets limpios en la carpeta: '{target}'...")
    for df_name, df_cleaned in dataframes.items():
        output_file_path = target / f"{df_name}.csv"
        df_cleaned.to_csv(
            output_file_path, index=False
        )  # index=False para no guardar el índice de pandas
        log.debug(f"  - '{df_name}.csv' guardado.")

    log.info("¡Todos los datasets limpios han sido guardados con éxito! ✅")
    return dataframes


# def merge_excel_csv(
#         dataframes_csv: dict[str, pd.DataFrame],
#         dataframes_excel: dict[str, pd.DataFrame],
#         target: pathlib.Path
# ) -> dict[str, pd.DataFrame]:
#     log.debug("Limpiando 'Assess_detail'...")
#     df_courses_excel = dataframes_excel[TablesExcelSchema.courses]
#     df_courses_csv = dataframes_csv[TablesCsvSchema.courses]
#     pd.merge
#     return dataframes


def clean_excel(
    dataframes: dict[str, pd.DataFrame], target: pathlib.Path
) -> dict[str, pd.DataFrame]:
    log.debug("Limpiando 'Assessment_detail'...")
    df_student_assessment = dataframes[TablesExcelSchema.assess_detail]
    df_student_assessment[AssessmentDetailExcel.score] = pd.to_numeric(
        df_student_assessment[AssessmentDetailExcel.score], errors="coerce"
    )
    df_student_assessment[AssessmentDetailExcel.score] = df_student_assessment[
        AssessmentDetailExcel.score
    ].fillna(0)
    df_student_assessment[AssessmentDetailExcel.date_submitted] = pd.to_numeric(
        df_student_assessment[AssessmentDetailExcel.date_submitted], errors="coerce"
    )
    df_student_assessment.dropna(
        subset=[AssessmentDetailExcel.date_submitted], inplace=True
    )
    dataframes[TablesExcelSchema.assess_detail] = df_student_assessment
    log.debug(f"  - 'Assessment_detail' limpio. Shape: {df_student_assessment.shape}")

    # DataFrame: studentInfo
    log.debug("Limpiando 'StudentInfo'...")
    df_student_info = dataframes[TablesExcelSchema.studentInfo]
    for field in [
        StudentInfoExcel.gender,
        StudentInfoExcel.region,
        StudentInfoExcel.highest_education,
        StudentInfoExcel.imd_band,
        StudentInfoExcel.age_band,
        StudentInfoExcel.disability,
        StudentInfoExcel.final_result,
    ]:
        df_student_info[field] = df_student_info[field].fillna(
            df_student_info[field].mode()[0]
        )

    df_student_info[StudentInfoExcel.num_of_prev_attempts] = df_student_info[
        StudentInfoExcel.num_of_prev_attempts
    ].fillna(df_student_info[StudentInfoExcel.num_of_prev_attempts].median())
    df_student_info[StudentInfoExcel.studied_credits] = df_student_info[
        StudentInfoExcel.studied_credits
    ].fillna(df_student_info[StudentInfoExcel.studied_credits].median())

    dataframes[TablesExcelSchema.studentInfo] = df_student_info
    log.debug(f"  - 'studentInfo' limpio. Shape: {df_student_info.shape}")

    # DataFrame: studentRegistration
    log.debug("Limpiando 'Registration'...")
    df_student_registration = dataframes[TablesExcelSchema.studentRegistration]
    df_student_registration[StudentRegistrationExcel.date_registration] = pd.to_numeric(
        df_student_registration[StudentRegistrationExcel.date_registration],
        errors="coerce",
    )
    df_student_registration[StudentRegistrationExcel.date_unregistration] = (
        pd.to_numeric(
            df_student_registration[StudentRegistrationExcel.date_unregistration],
            errors="coerce",
        )
    )

    df_student_registration[StudentRegistrationExcel.date_unregistration] = (
        df_student_registration[StudentRegistrationExcel.date_unregistration].fillna(-1)
    )
    df_student_registration.dropna(
        subset=[StudentRegistrationExcel.date_registration], inplace=True
    )
    dataframes[TablesExcelSchema.studentRegistration] = df_student_registration
    log.debug(f"  - 'Registration' limpio. Shape: {df_student_registration.shape}")

    # DataFrame: VLE_clickStream
    log.debug("Limpiando 'VLE_clickStream'...")
    df_student_vle = dataframes[TablesExcelSchema.studentVle]
    df_student_vle[StudentVleExcel.date] = pd.to_numeric(
        df_student_vle[StudentVleExcel.date], errors="coerce"
    )
    df_student_vle[StudentVleExcel.sum_clics] = pd.to_numeric(
        df_student_vle[StudentVleExcel.sum_clics], errors="coerce"
    )
    df_student_vle.dropna(
        subset=[StudentVleExcel.date, StudentVleExcel.sum_clics], inplace=True
    )
    dataframes[TablesExcelSchema.studentVle] = df_student_vle
    log.debug(f"  - 'VLE_clickStream' limpio. Shape: {df_student_vle.shape}")

    # DataFrame: vle
    log.debug("Limpiando 'Vle_modules'...")
    df_vle = dataframes[TablesExcelSchema.vle]
    df_vle[VleExcel.activity_type] = df_vle[VleExcel.activity_type].fillna(
        df_vle[VleExcel.activity_type].mode()[0]
    )
    df_vle[VleExcel.week_from] = pd.to_numeric(
        df_vle[VleExcel.week_from], errors="coerce"
    )
    df_vle[VleExcel.week_to] = pd.to_numeric(df_vle[VleExcel.week_to], errors="coerce")
    df_vle[VleExcel.week_from] = df_vle[VleExcel.week_from].fillna(-1)
    df_vle[VleExcel.week_to] = df_vle[VleExcel.week_to].fillna(-1)
    dataframes[TablesExcelSchema.vle] = df_vle
    log.debug(f"  - 'vle' limpio. Shape: {df_vle.shape}")

    log.info("Proceso de limpieza de datos completado. ✅")

    # --- 4. Guardar los DataFrames limpios en la nueva carpeta ---
    log.info(f"Guardando los datasets limpios en la carpeta: '{target}'...")
    for df_name, df_cleaned in dataframes.items():
        output_file_path = target / f"{df_name}.csv"
        df_cleaned.to_csv(
            output_file_path, index=False
        )  # index=False para no guardar el índice de pandas
        log.debug(f"  - '{df_name}.csv' guardado.")

    log.info("¡Todos los datasets limpios han sido guardados con éxito! ✅")
    return dataframes


def merge_csv(
    df_student_assessment: pd.DataFrame,
    df_assessments: pd.DataFrame,
    df_student_info: pd.DataFrame,
) -> pd.DataFrame:
    df_sa_detail = pd.merge(
        df_student_assessment,
        df_assessments,
        on=AssessmentsCsv.id_assessment,
        how="left",
        validate="many_to_many",
    )

    # Paso 2: unir con studentInfo (por id_student, code_module y code_presentation)
    # Mostrar ejemplo de columnas clave
    df_etl = pd.merge(
        df_student_info,
        df_sa_detail,
        on=[
            StudentInfoCsv.id_student,
            StudentInfoCsv.code_module,
            StudentInfoCsv.code_presentation,
        ],
        how="left",
        validate="many_to_many",
    )
    log.info(
        df_etl[
            [
                StudentInfoCsv.id_student,
                StudentInfoCsv.code_module,
                StudentInfoCsv.code_presentation,
                AssessmentsCsv.assessment_type,
                StudentAssessmentCsv.score,
            ]
        ].head()
    )
    return df_etl


def merge_excel(
    df_student_assessment: pd.DataFrame,
    df_assessments: pd.DataFrame,
    df_student_info: pd.DataFrame,
) -> pd.DataFrame:
    df_sa_detail = pd.merge(
        df_student_assessment,
        df_assessments,
        on=AssessmentsCsv.id_assessment,
        how="left",
        validate="many_to_many",
    )

    # Paso 2: unir con studentInfo (por id_student, code_module y code_presentation)
    # Mostrar ejemplo de columnas clave
    df_etl = pd.merge(
        df_student_info,
        df_sa_detail,
        on=[
            StudentInfoCsv.id_student,
            StudentInfoCsv.code_module,
            StudentInfoCsv.code_presentation,
        ],
        how="left",
        validate="many_to_many",
    )
    log.info(
        df_etl[
            [
                StudentInfoCsv.id_student,
                StudentInfoCsv.code_module,
                StudentInfoCsv.code_presentation,
                AssessmentsCsv.assessment_type,
                StudentAssessmentCsv.score,
            ]
        ].head()
    )
    return df_etl


def encode_as_ordinal(df_student_info: pd.DataFrame) -> pd.DataFrame:
    # Mapas ordinales para variables categóricas
    education_map = {
        "No Formal quals": 0,
        "Lower Than A Level": 1,
        "A Level or Equivalent": 2,
        "HE Qualification": 3,
        "Post Graduate Qualification": 4,
    }

    age_map = {"0-35": 0, "35-55": 1, "55<=": 2}

    imd_map = {
        "0-10%": 0,
        "10-20%": 1,
        "20-30%": 2,
        "30-40%": 3,
        "40-50%": 4,
        "50-60%": 5,
        "60-70%": 6,
        "70-80%": 7,
        "80-90%": 8,
        "90-100%": 9,
    }

    final_result_map = {"Withdrawn": 0, "Fail": 1, "Pass": 2, "Distinction": 3}

    df_student_info[StudentInfoCsv.highest_education_ord] = df_student_info[
        StudentInfoCsv.highest_education
    ].map(education_map)
    df_student_info[StudentInfoCsv.age_band_ord] = df_student_info[
        StudentInfoCsv.age_band
    ].map(age_map)
    df_student_info[StudentInfoCsv.imd_band_ord] = df_student_info[
        StudentInfoCsv.imd_band
    ].map(imd_map)
    df_student_info[StudentInfoCsv.final_result_ord] = df_student_info[
        StudentInfoCsv.final_result
    ].map(final_result_map)

    # Verificación del mapeo
    log.debug("Verificación de campos ordinales:")
    log.debug(
        df_student_info[
            [StudentInfoCsv.highest_education, StudentInfoCsv.highest_education_ord]
        ].drop_duplicates()
    )
    log.debug(
        df_student_info[
            [StudentInfoCsv.age_band, StudentInfoCsv.age_band_ord]
        ].drop_duplicates()
    )
    log.debug(
        df_student_info[
            [StudentInfoCsv.imd_band, StudentInfoCsv.imd_band_ord]
        ].drop_duplicates()
    )
    log.debug(
        df_student_info[
            [StudentInfoCsv.final_result, StudentInfoCsv.final_result_ord]
        ].drop_duplicates()
    )

    return df_student_info
