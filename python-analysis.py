"""
============================================================
Employee Retirement Benefits & Exposure Scenario Analysis
============================================================

Objective:
Assess how workforce demographics, compensation, tenure and
retirement assumptions influence projected retirement-benefit
exposure under illustrative scenarios.

Tools:
Python | Pandas | NumPy | Matplotlib

Dataset:
Synthetic HR workforce dataset.

Important:
This project is an illustrative scenario model for analytical
and portfolio purposes. It is NOT a professional actuarial
valuation and does not represent an actual pension liability.

Base-case assumptions:
- Analysis year: 2026
- Retirement age: 60
- Annual working hours: 2,080
- Annual salary growth: 6%
- Illustrative benefit accrual rate: 1.5%
============================================================
"""


# ============================================================
# 1. IMPORT LIBRARIES AND LOAD DATA
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("Retirement analysis dataset.csv")


# ============================================================
# 2. DATA CLEANING AND VALIDATION
# ============================================================

# Remove completely blank rows
df = df.dropna(how='all').copy()

# Check for duplicate employee IDs
duplicate_employee_ids = df['EmpID'].duplicated().sum()

# Validate employment status against termination indicator
employment_status_check = pd.crosstab(
    df['EmploymentStatus'],
    df['Termd']
)

# Validate termination dates against employment status
termination_date_check = pd.crosstab(
    df['EmploymentStatus'],
    df['DateofTermination'].isna()
)

# Convert date fields
df['DOB'] = pd.to_datetime(
    df['DOB'],
    format='mixed'
)

df['DateofHire'] = pd.to_datetime(
    df['DateofHire'],
    format='mixed'
)

# Correct two-digit DOB years that were interpreted as 20xx
df.loc[
    df['DOB'].dt.year > 2026,
    'DOB'
] -= pd.DateOffset(years=100)

# Validate that no employee's hire date precedes their DOB
invalid_hire_dates = (
    df['DateofHire'] < df['DOB']
).sum()


# ============================================================
# 3. WORKFORCE PREPARATION
# ============================================================

ANALYSIS_YEAR = 2026
BASE_RETIREMENT_AGE = 60
WORKING_HOURS_PER_YEAR = 2080
BASE_SALARY_GROWTH = 0.06
BASE_ACCRUAL_RATE = 0.015

# Calculate current age
df['Age'] = (
    ANALYSIS_YEAR - df['DOB'].dt.year
)

# Calculate years of service
df['YearsOfService'] = (
    ANALYSIS_YEAR - df['DateofHire'].dt.year
)

# Convert hourly pay rate to annual salary
# Assumption: 2,080 working hours per year
df['AnnualSalary'] = (
    df['PayRate'] * WORKING_HOURS_PER_YEAR
)

# Base-case retirement assumption
df['RetirementAge'] = BASE_RETIREMENT_AGE

# Calculate years remaining until retirement
# Negative values are capped at zero for employees already
# above the assumed retirement age.
df['YearsToRetirement'] = (
    df['RetirementAge'] - df['Age']
).clip(lower=0)


# ============================================================
# 4. RETIREMENT BENEFIT EXPOSURE MODEL
# ============================================================

# Project salary to assumed retirement age
df['SalaryGrowthRate'] = BASE_SALARY_GROWTH

df['ProjectedSalaryAtRetirement'] = (
    df['AnnualSalary']
    * (
        (1 + df['SalaryGrowthRate'])
        ** df['YearsToRetirement']
    )
)

# Project total years of service at retirement
df['ProjectedYearsOfService'] = (
    df['YearsOfService']
    + df['YearsToRetirement']
)

# Illustrative retirement benefit formula:
#
# Projected Benefit =
# Accrual Rate × Projected Years of Service
# × Projected Salary at Retirement
#
# This is a scenario estimate and not an actuarial valuation.

df['AccrualRate'] = BASE_ACCRUAL_RATE

df['ProjectedRetirementBenefit'] = (
    df['AccrualRate']
    * df['ProjectedYearsOfService']
    * df['ProjectedSalaryAtRetirement']
)


# ============================================================
# 5. CURRENT WORKFORCE EXPOSURE
# ============================================================

# Focus the analysis on the current workforce.
# Future starters and terminated employees are excluded.

df_model = df[
    df['EmploymentStatus'].isin(
        ['Active', 'Leave of Absence']
    )
].copy()

base_case_exposure = (
    df_model['ProjectedRetirementBenefit'].sum()
)

print("\nBASE-CASE RETIREMENT EXPOSURE")
print("-" * 45)
print(
    f"Current workforce: {len(df_model):,} employees"
)
print(
    f"Projected annual benefit exposure: "
    f"${base_case_exposure:,.2f}"
)


# ============================================================
# 6. AGE COHORT ANALYSIS
# ============================================================

df_model['AgeGroup'] = pd.cut(
    df_model['Age'],
    bins=[0, 39, 49, 59, 100],
    labels=[
        'Under 40',
        '40-49',
        '50-59',
        '60+'
    ]
)

age_analysis = (
    df_model
    .groupby(
        'AgeGroup',
        observed=False
    )
    .agg(
        Employees=(
            'Employee_Name',
            'count'
        ),
        TotalExposure=(
            'ProjectedRetirementBenefit',
            'sum'
        ),
        AverageExposure=(
            'ProjectedRetirementBenefit',
            'mean'
        )
    )
)

print("\nAGE COHORT ANALYSIS")
print("-" * 45)
print(age_analysis)


# ============================================================
# 7. CORRELATION ANALYSIS
# ============================================================

# Relationship between current workforce characteristics
# and years remaining until retirement.

workforce_correlation = df_model[
    [
        'Age',
        'AnnualSalary',
        'YearsToRetirement'
    ]
].corr()

# Relationship between projected salary and projected benefit
salary_benefit_correlation = df_model[
    [
        'ProjectedSalaryAtRetirement',
        'ProjectedRetirementBenefit'
    ]
].corr()

print("\nWORKFORCE CORRELATION ANALYSIS")
print("-" * 45)
print(workforce_correlation)

print("\nPROJECTED SALARY VS BENEFIT CORRELATION")
print("-" * 45)
print(salary_benefit_correlation)


# ============================================================
# 8. SALARY-GROWTH SENSITIVITY ANALYSIS
# ============================================================

# Test the effect of alternative annual salary growth assumptions.

df_model['Salary_4pct'] = (
    df_model['AnnualSalary']
    * (
        1.04 ** df_model['YearsToRetirement']
    )
)

df_model['Salary_6pct'] = (
    df_model['AnnualSalary']
    * (
        1.06 ** df_model['YearsToRetirement']
    )
)

df_model['Salary_8pct'] = (
    df_model['AnnualSalary']
    * (
        1.08 ** df_model['YearsToRetirement']
    )
)

# Calculate benefit exposure under each scenario

df_model['Benefit_4pct'] = (
    BASE_ACCRUAL_RATE
    * df_model['ProjectedYearsOfService']
    * df_model['Salary_4pct']
)

df_model['Benefit_6pct'] = (
    BASE_ACCRUAL_RATE
    * df_model['ProjectedYearsOfService']
    * df_model['Salary_6pct']
)

df_model['Benefit_8pct'] = (
    BASE_ACCRUAL_RATE
    * df_model['ProjectedYearsOfService']
    * df_model['Salary_8pct']
)

salary_growth_scenarios = {
    '4% Growth':
        df_model['Benefit_4pct'].sum(),

    '6% Growth':
        df_model['Benefit_6pct'].sum(),

    '8% Growth':
        df_model['Benefit_8pct'].sum()
}

print("\nSALARY GROWTH SENSITIVITY")
print("-" * 45)

for scenario, exposure in salary_growth_scenarios.items():
    print(
        f"{scenario}: ${exposure:,.2f}"
    )


# ============================================================
# 9. RETIREMENT-AGE SENSITIVITY ANALYSIS
# ============================================================

retirement_ages = [58, 60, 62]

for retirement_age in retirement_ages:

    years_to_retirement = (
        retirement_age - df_model['Age']
    ).clip(lower=0)

    service_at_retirement = (
        df_model['YearsOfService']
        + years_to_retirement
    )

    salary_at_retirement = (
        df_model['AnnualSalary']
        * (
            (1 + BASE_SALARY_GROWTH)
            ** years_to_retirement
        )
    )

    df_model[
        f'Benefit_{retirement_age}'
    ] = (
        BASE_ACCRUAL_RATE
        * service_at_retirement
        * salary_at_retirement
    )


retirement_age_scenarios = {
    'Age 58':
        df_model['Benefit_58'].sum(),

    'Age 60':
        df_model['Benefit_60'].sum(),

    'Age 62':
        df_model['Benefit_62'].sum()
}

print("\nRETIREMENT AGE SENSITIVITY")
print("-" * 45)

for scenario, exposure in retirement_age_scenarios.items():
    print(
        f"{scenario}: ${exposure:,.2f}"
    )


# ============================================================
# 10. DEPARTMENT ANALYSIS
# ============================================================

department_analysis = (
    df_model
    .groupby('Department')
    .agg(
        Employees=(
            'Employee_Name',
            'count'
        ),
        TotalExposure=(
            'ProjectedRetirementBenefit',
            'sum'
        ),
        AverageExposure=(
            'ProjectedRetirementBenefit',
            'mean'
        )
    )
    .sort_values(
        'TotalExposure',
        ascending=False
    )
)

print("\nDEPARTMENT EXPOSURE ANALYSIS")
print("-" * 45)
print(department_analysis)


# Department workforce profile

department_profile = (
    df_model
    .groupby('Department')
    .agg(
        Employees=(
            'Employee_Name',
            'count'
        ),
        AvgSalary=(
            'AnnualSalary',
            'mean'
        ),
        AvgAge=(
            'Age',
            'mean'
        ),
        AvgYearsOfService=(
            'YearsOfService',
            'mean'
        ),
        AvgYearsToRetirement=(
            'YearsToRetirement',
            'mean'
        ),
        AvgBenefit=(
            'ProjectedRetirementBenefit',
            'mean'
        )
    )
    .sort_values(
        'AvgBenefit',
        ascending=False
    )
)

print("\nDEPARTMENT WORKFORCE PROFILE")
print("-" * 45)
print(department_profile)


# ============================================================
# 11. VISUALISATIONS
# ============================================================


# ------------------------------------------------------------
# 11.1 Current Workforce Age Distribution
# ------------------------------------------------------------

age_bins = [
    30, 35, 40, 45, 50,
    55, 60, 65, 70, 75
]

age_labels = [
    '30–34',
    '35–39',
    '40–44',
    '45–49',
    '50–54',
    '55–59',
    '60–64',
    '65–69',
    '70–74'
]

age_distribution = (
    pd.cut(
        df_model['Age'],
        bins=age_bins,
        labels=age_labels,
        right=False
    )
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(9, 5))

bars = plt.bar(
    age_distribution.index,
    age_distribution.values
)

plt.title(
    'Current Workforce Age Distribution'
)
plt.xlabel('Age Group')
plt.ylabel('Number of Employees')

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f'{int(bar.get_height())}',
        ha='center',
        va='bottom'
    )

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 11.2 Projected Exposure by Age Group
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

bars = plt.bar(
    age_analysis.index.astype(str),
    age_analysis['TotalExposure']
)

plt.title(
    'Projected Retirement-Benefit Exposure by Age Group'
)
plt.xlabel('Age Group')
plt.ylabel(
    'Projected Annual Benefit Exposure ($)'
)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f'${bar.get_height() / 1_000_000:.2f}M',
        ha='center',
        va='bottom'
    )

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 11.3 Total Exposure by Department
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

bars = plt.bar(
    department_analysis.index,
    department_analysis['TotalExposure']
)

plt.title(
    'Projected Retirement-Benefit Exposure by Department'
)
plt.xlabel('Department')
plt.ylabel(
    'Projected Annual Benefit Exposure ($)'
)

plt.xticks(
    rotation=30,
    ha='right'
)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f'${bar.get_height() / 1_000_000:.2f}M',
        ha='center',
        va='bottom',
        fontsize=8
    )

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 11.4 Average Exposure per Employee by Department
# ------------------------------------------------------------

plt.figure(figsize=(9, 5))

bars = plt.bar(
    department_analysis.index,
    department_analysis['AverageExposure']
)

plt.title(
    'Average Projected Retirement Benefit by Department'
)
plt.xlabel('Department')
plt.ylabel(
    'Average Projected Annual Benefit ($)'
)

plt.xticks(
    rotation=30,
    ha='right'
)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f'${bar.get_height() / 1_000:.0f}K',
        ha='center',
        va='bottom',
        fontsize=8
    )

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 11.5 Salary-Growth Sensitivity
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

bars = plt.bar(
    salary_growth_scenarios.keys(),
    salary_growth_scenarios.values()
)

plt.title(
    'Retirement-Benefit Exposure Under Salary Growth Scenarios'
)
plt.xlabel('Annual Salary Growth')
plt.ylabel(
    'Projected Annual Benefit Exposure ($)'
)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f'${bar.get_height() / 1_000_000:.2f}M',
        ha='center',
        va='bottom'
    )

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 11.6 Retirement-Age Sensitivity
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

bars = plt.bar(
    retirement_age_scenarios.keys(),
    retirement_age_scenarios.values()
)

plt.title(
    'Retirement-Benefit Exposure Under Retirement-Age Scenarios'
)
plt.xlabel('Retirement Age')
plt.ylabel(
    'Projected Annual Benefit Exposure ($)'
)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f'${bar.get_height() / 1_000_000:.2f}M',
        ha='center',
        va='bottom'
    )

plt.tight_layout()
plt.show()


# ============================================================
# 12. KEY BUSINESS FINDINGS
# ============================================================

highest_total_department = (
    department_analysis['TotalExposure']
    .idxmax()
)

highest_average_department = (
    department_analysis['AverageExposure']
    .idxmax()
)

salary_4 = salary_growth_scenarios['4% Growth']
salary_6 = salary_growth_scenarios['6% Growth']
salary_8 = salary_growth_scenarios['8% Growth']

retirement_58 = retirement_age_scenarios['Age 58']
retirement_60 = retirement_age_scenarios['Age 60']
retirement_62 = retirement_age_scenarios['Age 62']

salary_growth_impact = (
    (salary_8 - salary_6)
    / salary_6
    * 100
)

print("\n")
print("=" * 65)
print("KEY BUSINESS FINDINGS")
print("=" * 65)

print(
    f"\n1. Base-case projected annual exposure: "
    f"${base_case_exposure:,.2f}"
)

print(
    f"   Current workforce included: "
    f"{len(df_model):,} employees"
)

print(
    f"\n2. Highest total departmental exposure: "
    f"{highest_total_department}"
)

print(
    f"   ${department_analysis.loc[highest_total_department, 'TotalExposure']:,.2f}"
)

print(
    f"\n3. Highest average exposure per employee: "
    f"{highest_average_department}"
)

print(
    f"   ${department_analysis.loc[highest_average_department, 'AverageExposure']:,.2f}"
)

print(
    f"\n4. Salary-growth sensitivity:"
)

print(
    f"   4% growth: ${salary_4:,.2f}"
)

print(
    f"   6% growth: ${salary_6:,.2f}"
)

print(
    f"   8% growth: ${salary_8:,.2f}"
)

print(
    f"   An increase from 6% to 8% raises "
    f"modelled exposure by approximately "
    f"{salary_growth_impact:.1f}%."
)

print(
    f"\n5. Retirement-age sensitivity:"
)

print(
    f"   Age 58: ${retirement_58:,.2f}"
)

print(
    f"   Age 60: ${retirement_60:,.2f}"
)

print(
    f"   Age 62: ${retirement_62:,.2f}"
)

print(
    "\n6. Key modelling takeaway:"
)

print(
    "   Projected retirement-benefit exposure is sensitive "
    "to salary growth and retirement-age assumptions, "
    "highlighting the importance of scenario analysis when "
    "assessing future workforce benefit exposure."
)

print("\n")
print("=" * 65)
print(
    "NOTE: Results are illustrative scenario estimates and "
    "should not be interpreted as professional actuarial "
    "valuations or actual pension liabilities."
)
print("=" * 65)
