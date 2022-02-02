import pandas as pd

#importing the data
read_file = pd.read_excel('data.xlsx')

#converting the excel file to csv
read_file.to_csv('data.csv', index = None,header=True)
#printing the first 10 rows
df = pd.DataFrame(pd.read_csv('data.csv'))

df