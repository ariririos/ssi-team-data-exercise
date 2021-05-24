import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.parser import parse, parserinfo
from dateutil.relativedelta import relativedelta
plt.close('all')

df = pd.read_csv('ssi-team-data-exercise-data-only.csv', index_col="Medicaid_ID")

''' Stacked bar plot for ACOs by quarter '''
df2 = df.groupby(['Submission Due Date', 'ACO_Name'])['ACO_Name'].count().unstack().fillna(0)
plt.figure()
df2.plot(kind='bar', stacked=True, xlabel='Quarter End Date', ylabel='ACO Counts', title='ACO Counts by Quarter', rot=0)

'''Stacked bar plot for service categories by quarter '''
df3 = df.groupby(['Submission Due Date', 'Service Category'])['Service Category'].count().unstack().fillna(0)
plt.figure()
df3.plot(kind='bar', stacked=True, xlabel='Quarter End Date', ylabel='Service Category Counts', title='Service Category Counts by Quarter', rot=0)

''' Pivot tables for demographic fields '''
demo_fields = ['Demo_Gender','Demo_Sexual_Orientation','Demo_Race','Demo_Language','Demo_Education','Demo_Employment']

for field in demo_fields:
    print('\nPivot table for ' + field)
    pivot_table = df.groupby([field])[field].count()
    pivot_table.to_csv('ssi-team-data-exercise-pivot-'+field+'.csv')
    print(pivot_table)

''' Aggregation and grouping by adult status, DOB >= 21 years ago '''
# Two-digit years 19 and lower are in the 2000s, 20 and above are in the 1900s
class TwentiethCenturyParserInfo(parserinfo):
    def convertyear(self, year, *args, **kwargs):
        if year > 19 and year < 100:
            year += 1900
        elif year <= 19:
            year += 2000
        return year

# Datetime logic from Stack Overflow community: https://stackoverflow.com/a/765990
def yearsago(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    return from_date - relativedelta(years=years)

def num_years(begin, end=None):
    if end is None:
        end = datetime.now()
    num_years = int((end - begin).days / 365.2425)
    if begin > yearsago(num_years, end):
        return num_years - 1
    else:
        return num_years

def over_21(dob):
    parsed = parse(dob, TwentiethCenturyParserInfo())
    return 'Adult' if num_years(parsed) >= 21 else 'Child'

df['adult'] = df['Member_Date_of_Birth'].apply(lambda dob: over_21(dob))

print('\nPivot table for adult status')
adult_pivot_table = df.groupby(['adult'])['adult'].count()
adult_pivot_table.to_csv('ssi-team-data-exercise-pivot-adult.csv')
print(adult_pivot_table)

plt.show()