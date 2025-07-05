import pathlib

import pandas as pd

from oulad_etl.etl.models import (
    Assessments,
    CoursesSchema,
    StudentAssessment,
    StudentInfo,
    StudentRegistration,
    StudentVle,
    TablesSchema,
    Vle,
)
from oulad_etl.log import log


def __clean_common_columns__(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia columnas comunes como 'code_module', 'code_presentation', 'id_student'
    convirtiéndolas a strings y eliminando espacios extra.
    """

    for col in [
        CoursesSchema.code_module,
        CoursesSchema.code_presentation,
        StudentInfo.id_student,
        Assessments.id_assessment,
        Vle.id_site,
    ]:
        if col in df.columns:
            # Convertir a string primero para manejar posibles nulos o tipos mixtos antes de strip
            df[col] = df[col].astype(str).str.strip()
    return df


def clean(
    dataframes: dict[str, pd.DataFrame], target: pathlib.Path
) -> dict[str, pd.DataFrame]:
    log.debug("Limpiando 'assessments'...")
    df_assessments = dataframes[TablesSchema.assessments]
    if Assessments.date in df_assessments.columns:
        df_assessments[Assessments.date] = pd.to_numeric(
            df_assessments[Assessments.date], errors="coerce"
        )
        df_assessments[Assessments.weight] = pd.to_numeric(
            df_assessments[Assessments.weight], errors="coerce"
        )
        df_assessments.dropna(
            subset=[Assessments.date, Assessments.weight], inplace=True
        )
        df_assessments[Assessments.weight] = df_assessments[Assessments.weight].fillna(
            df_assessments[Assessments.weight].mean()
        )
    df_assessments = __clean_common_columns__(df_assessments)
    dataframes[TablesSchema.assessments] = (
        df_assessments  # Actualizar el DataFrame limpio en el diccionario
    )

    log.debug(f"  - 'assessments' limpio. Shape: {df_assessments.shape}")

    # DataFrame: courses
    log.debug("Limpiando 'courses'...")
    df_courses = dataframes[TablesSchema.courses]
    df_courses = __clean_common_columns__(df_courses)
    dataframes[TablesSchema.courses] = df_courses
    log.debug(f"  - 'courses' limpio. Shape: {df_courses.shape}")

    # DataFrame: studentAssessment
    log.debug("Limpiando 'studentAssessment'...")
    df_student_assessment = dataframes[TablesSchema.studentAssessment]
    df_student_assessment[StudentAssessment.score] = pd.to_numeric(
        df_student_assessment[StudentAssessment.score], errors="coerce"
    )
    df_student_assessment[StudentAssessment.score] = df_student_assessment[
        StudentAssessment.score
    ].fillna(0)
    df_student_assessment[StudentAssessment.date_submitted] = pd.to_numeric(
        df_student_assessment[StudentAssessment.date_submitted], errors="coerce"
    )
    df_student_assessment.dropna(
        subset=[StudentAssessment.date_submitted], inplace=True
    )
    df_student_assessment = __clean_common_columns__(df_student_assessment)
    dataframes[TablesSchema.studentAssessment] = df_student_assessment
    log.debug(f"  - 'studentAssessment' limpio. Shape: {df_student_assessment.shape}")

    # DataFrame: studentInfo
    log.debug("Limpiando 'studentInfo'...")
    df_student_info = dataframes[TablesSchema.studentInfo]
    for field in [
        StudentInfo.gender,
        StudentInfo.region,
        StudentInfo.highest_education,
        StudentInfo.imd_band,
        StudentInfo.age_band,
        StudentInfo.disability,
        StudentInfo.final_result,
    ]:
        df_student_info[field] = df_student_info[field].fillna(
            df_student_info[field].mode()[0]
        )

    df_student_info[StudentInfo.imd_band] = df_student_info[
        StudentInfo.imd_band
    ].replace("10-20", "10-20%")
    df_student_info[StudentInfo.num_of_prev_attempts] = df_student_info[
        StudentInfo.num_of_prev_attempts
    ].fillna(df_student_info[StudentInfo.num_of_prev_attempts].median())
    df_student_info[StudentInfo.studied_credits] = df_student_info[
        StudentInfo.studied_credits
    ].fillna(df_student_info[StudentInfo.studied_credits].median())

    df_student_info = __clean_common_columns__(df_student_info)
    dataframes[TablesSchema.studentInfo] = df_student_info
    log.debug(f"  - 'studentInfo' limpio. Shape: {df_student_info.shape}")

    # DataFrame: studentRegistration
    log.debug("Limpiando 'studentRegistration'...")
    df_student_registration = dataframes[TablesSchema.studentRegistration]
    df_student_registration[StudentRegistration.date_registration] = pd.to_numeric(
        df_student_registration[StudentRegistration.date_registration], errors="coerce"
    )
    df_student_registration[StudentRegistration.date_unregistration] = pd.to_numeric(
        df_student_registration[StudentRegistration.date_unregistration],
        errors="coerce",
    )

    df_student_registration[StudentRegistration.date_unregistration] = (
        df_student_registration[StudentRegistration.date_unregistration].fillna(-1)
    )
    df_student_registration.dropna(
        subset=[StudentRegistration.date_registration], inplace=True
    )
    df_student_registration = __clean_common_columns__(df_student_registration)
    dataframes[TablesSchema.studentRegistration] = df_student_registration
    log.debug(
        f"  - 'studentRegistration' limpio. Shape: {df_student_registration.shape}"
    )

    # DataFrame: studentVle
    log.debug("Limpiando 'studentVle'...")
    df_student_vle = dataframes[TablesSchema.studentVle]
    df_student_vle[StudentVle.date] = pd.to_numeric(
        df_student_vle[StudentVle.date], errors="coerce"
    )
    df_student_vle[StudentVle.sum_click] = pd.to_numeric(
        df_student_vle[StudentVle.sum_click], errors="coerce"
    )
    df_student_vle.dropna(subset=[StudentVle.date, StudentVle.sum_click], inplace=True)
    df_student_vle = __clean_common_columns__(df_student_vle)
    dataframes[TablesSchema.studentVle] = df_student_vle
    log.debug(f"  - 'studentVle' limpio. Shape: {df_student_vle.shape}")

    # DataFrame: vle
    log.debug("Limpiando 'vle'...")
    df_vle = dataframes[TablesSchema.vle]
    df_vle[Vle.activity_type] = df_vle[Vle.activity_type].fillna(
        df_vle[Vle.activity_type].mode()[0]
    )
    df_vle[Vle.week_from] = pd.to_numeric(df_vle[Vle.week_from], errors="coerce")
    df_vle[Vle.week_to] = pd.to_numeric(df_vle[Vle.week_to], errors="coerce")
    df_vle[Vle.week_from] = df_vle[Vle.week_from].fillna(-1)
    df_vle[Vle.week_to] = df_vle[Vle.week_to].fillna(-1)
    df_vle = __clean_common_columns__(df_vle)
    dataframes[TablesSchema.vle] = df_vle
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


def merge(
    df_student_assessment: pd.DataFrame,
    df_assessments: pd.DataFrame,
    df_student_info: pd.DataFrame,
) -> pd.DataFrame:
    df_sa_detail = pd.merge(
        df_student_assessment,
        df_assessments,
        on=Assessments.id_assessment,
        how="left",
        validate="many_to_many",
    )

    # Paso 2: unir con studentInfo (por id_student, code_module y code_presentation)
    # Mostrar ejemplo de columnas clave
    df_etl = pd.merge(
        df_student_info,
        df_sa_detail,
        on=[
            StudentInfo.id_student,
            StudentInfo.code_module,
            StudentInfo.code_presentation,
        ],
        how="left",
        validate="many_to_many",
    )
    log.info(
        df_etl[
            [
                StudentInfo.id_student,
                StudentInfo.code_module,
                StudentInfo.code_presentation,
                Assessments.assessment_type,
                StudentAssessment.score,
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

    df_student_info[StudentInfo.highest_education_ord] = df_student_info[
        StudentInfo.highest_education
    ].map(education_map)
    df_student_info[StudentInfo.age_band_ord] = df_student_info[
        StudentInfo.age_band
    ].map(age_map)
    df_student_info[StudentInfo.imd_band_ord] = df_student_info[
        StudentInfo.imd_band
    ].map(imd_map)
    df_student_info[StudentInfo.final_result_ord] = df_student_info[
        StudentInfo.final_result
    ].map(final_result_map)

    # Verificación del mapeo
    log.debug("Verificación de campos ordinales:")
    log.debug(
        df_student_info[
            [StudentInfo.highest_education, StudentInfo.highest_education_ord]
        ].drop_duplicates()
    )
    log.debug(
        df_student_info[
            [StudentInfo.age_band, StudentInfo.age_band_ord]
        ].drop_duplicates()
    )
    log.debug(
        df_student_info[
            [StudentInfo.imd_band, StudentInfo.imd_band_ord]
        ].drop_duplicates()
    )
    log.debug(
        df_student_info[
            [StudentInfo.final_result, StudentInfo.final_result_ord]
        ].drop_duplicates()
    )

    return df_student_info
