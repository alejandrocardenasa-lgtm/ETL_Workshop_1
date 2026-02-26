# Dimension tables
CREATE TABLE dim_candidate (
  candidate_key INT PRIMARY KEY,
  first_name    VARCHAR(100),
  last_name     VARCHAR(100),
  email         VARCHAR(150),
  country       VARCHAR(100)
);

CREATE TABLE dim_date (
  date_key   INT PRIMARY KEY,
  full_date  DATE,
  year       INT,
  month      INT,
  day        INT
);

CREATE TABLE dim_seniority (
  seniority_key INT PRIMARY KEY,
  seniority     VARCHAR(50)
);

CREATE TABLE dim_technology (
  technology_key INT PRIMARY KEY,
  technology     VARCHAR(100)
);

# Fact table
CREATE TABLE fact_applications (
  application_key INT AUTO_INCREMENT PRIMARY KEY,

  candidate_key   INT,
  date_key        INT,
  seniority_key   INT,
  technology_key  INT,

  years_of_experience       INT,
  code_challenge_score      DECIMAL(5,2),
  technical_interview_score DECIMAL(5,2),
  hired_flag                INT,

  FOREIGN KEY (candidate_key)  REFERENCES dim_candidate(candidate_key),
  FOREIGN KEY (date_key)       REFERENCES dim_date(date_key),
  FOREIGN KEY (seniority_key)  REFERENCES dim_seniority(seniority_key),
  FOREIGN KEY (technology_key) REFERENCES dim_technology(technology_key)
);