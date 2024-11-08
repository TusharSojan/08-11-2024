import pandas as pd
from datetime import datetime

# Load CSV files
departments = pd.read_csv("departments.csv")
dept_emp = pd.read_csv("dept_emp.csv")
dept_manager = pd.read_csv("dept_manager.csv")
employees = pd.read_csv("employees.csv")
salaries = pd.read_csv("salaries.csv")
titles = pd.read_csv("titles.csv")

# Parse dates - Specify the correct format
employees['hire_date'] = pd.to_datetime(employees['hire_date'], format='%Y-%m-%d', errors='coerce')
dept_emp['from_date'] = pd.to_datetime(dept_emp['from_date'], format='%Y-%m-%d', errors='coerce')
dept_emp['to_date'] = pd.to_datetime(dept_emp['to_date'], format='%Y-%m-%d', errors='coerce')
salaries['from_date'] = pd.to_datetime(salaries['from_date'], format='%Y-%m-%d', errors='coerce')
salaries['to_date'] = pd.to_datetime(salaries['to_date'], format='%Y-%m-%d', errors='coerce')
titles['from_date'] = pd.to_datetime(titles['from_date'], format='%Y-%m-%d', errors='coerce')
titles['to_date'] = pd.to_datetime(titles['to_date'], format='%Y-%m-%d', errors='coerce')

# 1. Max Salary and Latest Salary
# Group by emp_no to get max salary and the most recent salary
max_salary = salaries.groupby('emp_no')['salary'].max().reset_index(name='max_salary')
latest_salary = salaries.sort_values('from_date').groupby('emp_no').tail(1)[['emp_no', 'salary']].rename(columns={'salary': 'latest_salary'})

# Merge max and latest salary with employees
salary_data = pd.merge(max_salary, latest_salary, on='emp_no', how='left')

# 2. Last Working Date and Current Employment Status
# Get the last working date from dept_emp
last_working = dept_emp.sort_values('to_date').groupby('emp_no').tail(1)[['emp_no', 'to_date']]
# Mark employees with 9999-01-01 as currently employed
last_working['current_employee'] = last_working['to_date'].apply(lambda x: x == datetime(9999, 1, 1))

# Merge last working date with employees
employment_data = pd.merge(employees, last_working, on='emp_no', how='left')

# 3. Years of Experience Calculation
employment_data['years_experience'] = ((employment_data['to_date'] - employment_data['hire_date']).dt.days / 365).fillna(0).astype(int)

# 4. Current Title
# Filter titles to get the latest title for each employee
latest_title = titles.sort_values('from_date').groupby('emp_no').tail(1)[['emp_no', 'title']]

# Merge everything into a final DataFrame
final_data = employment_data.merge(salary_data, on='emp_no', how='left')
final_data = final_data.merge(latest_title, on='emp_no', how='left')

# Select the required columns
final_data = final_data[['first_name', 'max_salary', 'latest_salary', 'hire_date', 'to_date', 'current_employee', 'years_experience', 'title']]

# Display the final result
print(final_data)
