import pandas as pd

def transform(df: pd.DataFrame):

    df = df.copy()

    df["hired_flag"] = (
        (df["Code Challenge Score"] >= 7) &
        (df["Technical Interview Score"] >= 7)
    ).astype(int)

    df["Email"] = df["Email"].astype(str).str.strip()
    df = df[df["Email"].notna() & (df["Email"] != "")]
    df = df[df["Application Date"].notna()]

    df["First Name"] = df["First Name"].astype(str).str.strip().str.title()
    df["Last Name"] = df["Last Name"].astype(str).str.strip().str.title()
    df["Country"] = df["Country"].astype(str).str.strip().str.upper()
    df["Seniority"] = df["Seniority"].astype(str).str.strip().str.title()
    df["Technology"] = df["Technology"].astype(str).str.strip().str.title()

    df["YOE"] = pd.to_numeric(df["YOE"], errors="coerce").fillna(0).astype(int)
    df["Code Challenge Score"] = pd.to_numeric(df["Code Challenge Score"], errors="coerce").fillna(0).astype(float)
    df["Technical Interview Score"] = pd.to_numeric(df["Technical Interview Score"], errors="coerce").fillna(0).astype(float)

    df = df.drop_duplicates(subset=["Email", "Application Date", "Seniority", "Technology"])

    dim_candidate = (
        df[["First Name", "Last Name", "Email", "Country"]]
        .drop_duplicates(subset=["Email"])
        .sort_values("Email")
        .reset_index(drop=True)
    )
    dim_candidate["candidate_key"] = dim_candidate.index + 1
    dim_candidate = dim_candidate.rename(
        columns={
            "First Name": "first_name",
            "Last Name": "last_name",
            "Email": "email",
            "Country": "country",
        }
    )[["candidate_key", "first_name", "last_name", "email", "country"]]

    dim_date = (
        df[["Application Date"]]
        .drop_duplicates()
        .rename(columns={"Application Date": "full_date"})
        .sort_values("full_date")
        .reset_index(drop=True)
    )
    dim_date["date_key"] = dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["year"] = dim_date["full_date"].dt.year
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date = dim_date[["date_key", "full_date", "year", "month", "day"]]

    dim_seniority = (
        df[["Seniority"]]
        .drop_duplicates()
        .sort_values("Seniority")
        .reset_index(drop=True)
        .rename(columns={"Seniority": "seniority"})
    )
    dim_seniority["seniority_key"] = dim_seniority.index + 1
    dim_seniority = dim_seniority[["seniority_key", "seniority"]]

    dim_technology = (
        df[["Technology"]]
        .drop_duplicates()
        .sort_values("Technology")
        .reset_index(drop=True)
        .rename(columns={"Technology": "technology"})
    )
    dim_technology["technology_key"] = dim_technology.index + 1
    dim_technology = dim_technology[["technology_key", "technology"]]

    fact = df.rename(
        columns={
            "Email": "email",
            "Application Date": "application_date",
            "YOE": "years_of_experience",
            "Code Challenge Score": "code_challenge_score",
            "Technical Interview Score": "technical_interview_score",
            "Seniority": "seniority",
            "Technology": "technology",
        }
    )[
        [
            "email",
            "application_date",
            "seniority",
            "technology",
            "years_of_experience",
            "code_challenge_score",
            "technical_interview_score",
            "hired_flag",
        ]
    ].copy()

    fact["date_key"] = fact["application_date"].dt.strftime("%Y%m%d").astype(int)
    fact = fact.drop(columns=["application_date"])

    fact = fact.merge(dim_candidate[["candidate_key", "email"]], on="email", how="left")
    fact = fact.merge(dim_seniority, on="seniority", how="left")
    fact = fact.merge(dim_technology, on="technology", how="left")

    fact_applications = fact[
        [
            "candidate_key",
            "date_key",
            "seniority_key",
            "technology_key",
            "years_of_experience",
            "code_challenge_score",
            "technical_interview_score",
            "hired_flag",
        ]
    ].copy()

    return dim_candidate, dim_date, dim_seniority, dim_technology, fact_applications