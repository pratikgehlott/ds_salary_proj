# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 08:09:31 2020

@author: Gehlot Pratik
"""

import pandas as pd

df = pd.read_csv('glassdoor_jobs.csv')

#salary parsing
#Removing -1 values from the column
df = df[df['Salary Estimate'] != '-1']

#Parsing salary column to remove text "glassdoor_estimate"
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
#parsing salary column to remove text "K"  and "dollar sign"
minus_Kd = salary.apply(lambda x: x.replace('K','').replace("$", ''))

#parsing minus_Kd column to deal with "per hour" values and "employeer provided salary" text
min_hr = minus_Kd.apply(lambda x : x.lower().replace('per hour', '').replace('employer provided salary:', ''))

#min salary and max salaryg'] <0 else x['Company Name
df['min_salary'] = min_hr.apply(lambda x:int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x:int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary + df.max_salary)/2



#Company name text only
#axis = 1 to tell python we are doing on rows
df['company_txt'] = df.apply(lambda x:x['Company Name'] if x['Rating'] <0 else x['Company Name'][:-3],axis = 1)
 
#state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])

#location == headquarters would be a great data point
df['same_state'] = df.apply(lambda x: 1 if x.Location== x.Headquarters else 0, axis =1 )


#age of company
df['age'] = df.Founded.apply(lambda x:x if x<1 else 2020 - x)

#parsing of job description (python, etc)

#python (checking if any of the job description has python)

df['python_yn'] = df['Job Description'].apply(lambda x : 1 if 'python' in x.lower() else 0)


#same for r-studio
df['R_yn'] = df['Job Description'].apply(lambda x : 1 if 'r studio' in x.lower()  or 'r-studio' in x.lower() else 0)


#same for spark
df['spark'] = df['Job Description'].apply(lambda x : 1 if 'spark' in x.lower() else 0)

#same for aws
df['aws'] = df['Job Description'].apply(lambda x : 1 if 'aws' in x.lower() else 0)

#same for excel
df['excel'] = df['Job Description'].apply(lambda x : 1 if 'excel' in x.lower() else 0)

#droping useless column
df_out = df.drop(['Unnamed: 0'], axis = 1)

df_out.to_csv('salary_data_cleaned.csv', index = False)



















