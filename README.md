# Employee Retirement Benefits & Exposure Scenario Analysis

## Overview

This project uses Python to analyze workforce demographics, compensation, tenure, and retirement assumptions to estimate illustrative annual retirement-benefit exposure under different scenarios.

The analysis is designed as a simplified business analytics and scenario-modeling exercise inspired by retirement consulting.

> Important:This is an illustrative scenario model, not a professional actuarial valuation or a calculation of actual pension liabilities.

---

## Business Question

How could an organization's workforce demographics, compensation, tenure, and retirement assumptions affect its future employee retirement-benefit exposure?

---

## Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- Excel

---

## Dataset

The project uses the Human Resources Data Set — Dental Magic dataset from Kaggle.

The dataset is synthetic/fictitious and contains employee-level information including:

- Date of birth
- Date of hire
- Pay rate
- Department
- Employment status
- Termination information
- Job position

For this analysis, the model focuses primarily on employees who are currently Active or on Leave of Absence.

---

## Methodology

### 1. Workforce Filtering

The analysis focuses on the current workforce:

- Active employees
- Employees on Leave of Absence

Future-start employees and terminated employees are excluded from the primary exposure analysis.

### 2. Compensation

Hourly pay rates are converted into annual salary using:

**Annual Salary = Hourly Pay Rate × 2,080 hours**

### 3. Retirement Projection

The base scenario assumes:

| Assumption                   | Base Case |
| Analysis year                | 2026 |
| Retirement age               | 60 |
| Annual salary growth         | 6% |
| Illustrative accrual rate    | 1.5% |
| Working hours per year       | 2,080 |

### 4. Projected Salary

Salary at retirement is estimated using:

Projected Salary = Current Annual Salary × (1 + Salary Growth Rate)^Years to Retirement

### 5. Illustrative Retirement Benefit

The simplified annual benefit estimate is:

Projected Benefit = Accrual Rate × Projected Years of Service × Projected Salary at Retirement

This formula is used only for scenario analysis and does not represent the rules of an actual pension plan.

---

## Key Findings

### Base Case

Under the base assumptions of:

- Retirement age: 60
- Salary growth: 6%
- Accrual rate: 1.5%

the current workforce produces approximately:

$14.39M in projected annual retirement-benefit exposure

under the illustrative model.

### Salary Growth Sensitivity

Changing the assumed annual salary growth produces substantial differences:

| Salary Growth | Projected Exposure |
| 4%            | $10.29M            |
| 6%            | $14.39M            |
| 8%            | $20.24M            |

The model therefore demonstrates how strongly long-term benefit projections can depend on salary-growth assumptions.

### Retirement Age Sensitivity

Holding salary growth at 6%:

| Retirement Age | Projected Exposure |
| 58             | $12.00M |
| 60             | $14.39M |
| 62             | $17.22M |

Under this simplified benefit formula, later retirement increases projected annual benefit because it allows additional service accumulation and salary growth.

### Workforce Segmentation

Production has the largest total modeled exposure because it represents the largest employee group.

Sales has the highest average modeled exposure per employee among the larger departments, reflecting its relatively higher average compensation and remaining years to retirement.

---

## Visualizations

### Current Workforce Age Distribution

![Current Workforce Age Distribution](current%20workforce%20age%20distribution.png)

### Projected Retirement Benefit Exposure by Age Group

![Projected Retirement Benefit Exposure by Age Group](Projected%20Retirement%20Benefit%20Exposure%20by%20Age%20group.png)

### Projected Retirement Benefit Exposure by Department

![Projected Retirement Benefit Exposure by Department](Projected%20Retirement%20Benefit%20Exposure%20by%20Dept%20.png)

### Average Projected Retirement Benefit by Department

![Average Projected Retirement Benefit by Department](Average%20Projected%20Retirement%20Benefit%20by%20Department%20.png)

### Salary Growth Sensitivity

![Retirement Benefit Exposure under Salary Growth Scenarios](Retirement%20Benefit%20Exposure%20under%20Salary%20Growth%20Scenarios.png)

### Retirement Age Sensitivity

![Retirement Benefit Exposure under Retirement Age Scenarios](Retirement%20Benefit%20Exposure%20under%20retirement%20age%20scenarios.png)

## Key Analytical Takeaways

1. Salary growth is a major driver of modeled retirement-benefit exposure.
2. Workforce size and average compensation both influence total departmental exposure.
3. Younger employees can generate higher modeled exposure under long-term salary-compounding assumptions.
4. Scenario analysis is important because retirement projections are highly sensitive to assumptions.
5. The results should be interpreted as analytical scenarios rather than actual pension liabilities.

---

## Limitations

This project intentionally uses a simplified scenario model.

It does not incorporate:

- Discounted present value
- Mortality assumptions
- Employee turnover or future workforce changes
- Vesting rules
- Inflation
- Pension plan-specific eligibility rules
- Benefit caps
- Employee contributions
- Employer contributions
- Actual plan documents or actuarial assumptions

The underlying dataset is synthetic/fictitious.

---

## Project Structure
employee-retirement-benefits-analysis/
│
├── README.md
├── python-analysis.py
├── Retirement analysis dataset.csv
└── visualizations/

pip install pandas numpy matplotlib
python python-analysis.py
