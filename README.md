# Workshop 1 - ETL Data Engineer

## Description

This project corresponds to **Workshop 1** of the course **ETL (G01)** in the **Data Engineering and Artificial Intelligence** program.
It simulates a real technical interview challenge for a **Data Engineer** role, implementing a complete end-to-end ETL process:

<img width="1025" height="468" alt="image" src="https://github.com/user-attachments/assets/c93486d5-71f0-48bf-b89a-e74070c34897" />

1. **Extract** → Load a dataset of candidates from a CSV file.
2. **Transform** → Data cleaning, validation, business rules (*HIRED* rule), and the design of a **dimensional model (star schema)**.
3. **Load** → Load the resulting tables into a **MySQL Data Warehouse**.
4. **Reporting** → Calculate **KPIs** and generate reports from the Data Warehouse (not directly from the CSV).

---

## Dimensional Model (Star Schema)

<img width="741" height="638" alt="workshop drawio" src="https://github.com/user-attachments/assets/080bc097-dc57-42bd-9e51-b9016e7f56f5" />

The schema consists of a fact table (`fact_selection`) and five dimension tables (`dim_candidate`, `dim_technology`, `dim_country`, `dim_seniority`, `dim_date`).

**Fact Table: FactSelection**
The central table that records the events of each selection process. It contains the following metrics and foreign keys:

* **Metrics:**

  * `code_challenge_score` (technical test score).
  * `technical_interview_score` (technical interview score).
  * `hired (0/1)` (hire indicator).

* **Foreign Keys:** Link each fact to its related dimensions (candidate, date, country, technology, seniority).

This table enables KPIs such as:

* Hiring rate.
* Hires by technology, country, seniority, or year.
* Average test and interview scores.

**Dimension Tables:**

* **DimCandidate:** candidate attributes (name, email, years of experience). Enables segmentation by applicant profile.
* **DimTechnology:** records evaluated technologies and helps measure demand and success rates by tech stack.
* **DimCountry:** stores candidates’ countries of origin and supports international comparisons.
* **DimSeniority:** defines experience levels (Junior, Semi-Senior, Senior), useful for analyzing hiring trends by seniority.
* **DimDate:** stores application dates (day, month, year), supporting time-based analysis.

**Model Justification:**
The star schema design follows common best practices in Data Warehousing for its simplicity and efficiency:

* **Analytical Clarity:** separates numerical measures (facts) from descriptive attributes (dimensions).
* **Scalability:** allows adding new dimensions (e.g., recruitment source) without redesigning the model.
* **Performance:** optimizes frequent aggregation queries and filtering for KPIs.
* **Reusability:** dimensions can be reused if new business processes are added in the DW.

---

## ETL Pipeline

### 1. Extract

* Input file: `data/candidates.csv` (50k records).
* Initial exploration in `notebook/eda.ipynb` (check for nulls, duplicates, invalid emails, etc.).

### 2. Transform

* Implemented in `src/ETL/transform.py`.
* Transformation rules:

  * **`hired` column:** A candidate is considered hired if `Code Challenge Score ≥ 7` and `Technical Interview Score ≥ 7`.
  * Creation of dimensions and primary keys.
  * Generation of the `fact_selection` table.

### 3. Load

* Implemented in `src/ETL/load.py`.
* Automated loading into **MySQL Workbench** (`selection_dw`):

  * Database creation (`selection_dw`).
  * Data insertion using `mysql-connector-python`.

### 4. KPIs & Reporting

* Implemented in `src/ETL/kpis.py`.
* Metrics calculated:

  1. **Hiring Rate (% of hires).**
  2. **Average challenge and interview scores by seniority.**
  3. **Hires by technology.**
  4. **Hires by year.**
  5. **Hires by seniority.**
  6. **Hires by country over time** (focus: USA, Brazil, Colombia, Ecuador).

---

## Repository Structure

```bash
WORKSHOP1/
│── data/
│   └── candidates.csv          # Original dataset
│── notebook/
│   └── eda.ipynb               # Initial exploration (EDA)
│── src/
│   └── ETL/
│       ├── transform.py        # Transformation and dimensional model creation
│       ├── load.py             # Load to MySQL DW
│       ├── kpis.py             # SQL queries and KPIs
│       └── main.py             # ETL Orchestration (Extract → Transform → Load)
│── requirements.txt            # Required libraries
```

## Technologies Used

* **Jupyter Notebook** → Exploratory Data Analysis (EDA).
* **Python** (3.x)

  * `pandas`, `numpy` → Data transformation.
  * `mysql-connector-python` → MySQL connection.
* **MySQL Workbench** → Data Warehouse (DW).
* **Power BI** → KPI visualization and interactive dashboards.

## Key Decisions

* **Star Schema:**
  Chosen for its wide adoption in analytics. It allows quick, intuitive queries and simplifies the integration of multiple dimensions (candidate, date, country, technology, seniority) around a central fact table.

* **MySQL Workbench as Data Warehouse:**
  Selected for being lightweight, widely used, and Python-compatible. This ensures the project can be easily replicated across environments.

* **KPI Selection:**
  The KPIs reflect strategic insights into the recruitment process:

  * **Hiring Rate:** measures efficiency.
  * **Average scores by seniority:** reflects candidate quality.
  * **Hires by technology, seniority, and country:** provide comparative insights.
  * **Hires by year:** reveal historical trends.

* **Power BI for Dashboards:**
  Chosen for its strong industry adoption and integration with MySQL. It enables dynamic, intuitive dashboards for both technical and non-technical users and supports collaborative publishing.

---

## Installation & Execution

1. Clone the repository:

   ```bash
   git clone https://github.com/Mariana-Cifuentes/Workshop1.git
   cd WORKSHOP1
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. Configure MySQL Workbench:

   * Create database `selection_dw`.
   * Update credentials in `src/ETL/main.py` and `src/ETL/kpis.py` (host, user, password).

4. Run the full ETL pipeline:

   ```bash
   python src/ETL/main.py
   ```

5. Query KPIs:

   ```bash
   python src/ETL/kpis.py
   ```

---

## Results

The KPIs provide insights into the recruitment process:

* Distribution of hires by **technology, seniority, country, and year**.
* Overall **Hiring Rate**.
* Average scores of hired candidates by **seniority**.

This delivers a **strategic view** of how hiring evolves across different contexts.

---

## Visualizations (Power BI)

A **Power BI dashboard** was built and connected to the MySQL Data Warehouse, enabling analysis of the project’s KPIs.

<img width="1602" height="889" alt="image" src="https://github.com/user-attachments/assets/e08e7e67-0089-4a16-9ede-e82280ca88fe" />

[View Dashboard Online](https://app.powerbi.com/groups/me/reports/fdfa3a94-378a-4fd5-a866-0af8d9ddfd82/18b7e5a9665e905b2b7a?ctid=693cbea0-4ef9-4254-8977-76e05cb5f556&experience=power-bi)

### Hires by Year

The chart shows candidate hires between 2018 and 2022:

* 2018–2019: steady growth, peaking in 2019 with over 1,500 hires.
* 2020–2021: stable around 1,480–1,500 hires.
* 2022: significant drop, with fewer than 1,000 hires.

**Analysis:**
The initial growth reflects strong demand for tech profiles. Stability during 2020–2021 shows sector resilience despite the pandemic. The sharp decline in 2022 suggests market contraction due to workforce adjustments or reduced investment.

---

### Hires by Year and Country

The chart shows hiring trends in Brazil, Colombia, Ecuador, and the US (2018–2022):

* **Brazil:** started highest in 2018, steadily declined through 2022.
* **Colombia:** stable until 2020, then a sharp drop in 2021.
* **Ecuador:** steady growth until 2020 peak, then gradual decline.
* **United States:** initial drop in 2019, then strong growth, peaking in 2021, followed by a decline in 2022.

**Analysis:**

* Brazil and Colombia faced reduced hiring by the end of the period.
* Ecuador showed early growth but could not sustain it.
* The US demonstrated the strongest recovery, with notable growth from 2020 onwards.

---

### Hires by Seniority Level

* Interns: 985 hires (highest).
* Juniors: 977, Trainees: 973, Architects: 971.
* Senior (939), Lead (929), and Mid-Level (924) slightly lower.

**Analysis:**
Companies prefer early-career talent (interns, juniors, trainees), possibly due to:

* Lower costs.
* Flexibility.
* Opportunity to train internally.

Experienced profiles are also hired in significant numbers, but hiring skews towards entry-level roles.

---

### Hires by Technology

* **Top demand:** Game Development (519), DevOps (495).
* **Strong demand:** System Administration, CMS Backend, Adobe Experience Manager, Database Administration (\~280–293).
* **Moderate demand:** Frontend, QA, Security, Salesforce, Data Engineer (\~250–270).
* **Lower demand:** Social Media Community Management (237), Technical Writing (223).

**Analysis:**
Critical technical roles dominate:

* Game Development reflects digital entertainment growth.
* DevOps/System Admin ensure system reliability.
* Roles tied to communication/documentation show lower demand.

---

### Hires vs. Not Hired

* **Not Hired:** 43k (86.6%).
* **Hires:** 7k (13.4%).

**Analysis:**
Most candidates don’t meet the threshold (≥7 in test and interview). Hiring is highly selective.

---

### Average Scores by Seniority (Challenge vs. Interview)

* All levels: averages \~8.4–8.5.
* No major differences between test and interview.
* Leads/Architects slightly lower in test scores.
* Entry-level roles nearly identical across both.

**Analysis:**

* The ≥7 threshold ensures consistency.
* Hired candidates perform well above the minimum.
* Results highlight uniform quality among hires.

---
