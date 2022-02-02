import pandas as pd
from datetime import datetime, date 
import warnings
warnings.filterwarnings('ignore')

#reading the data
read_data = pd.read_csv('data.csv',skiprows=1,sep = ',')

read_data['PO_date'] = pd.to_datetime(read_data.PO_date, infer_datetime_format=True)
#printing the first rows
print(read_data.head(10))
print('\n')
print('The columns are: ')
print(read_data.columns.tolist())
#converting the date field from string to datetime
read_data['PO_date'] = pd.to_datetime(read_data['PO_date'],errors='coerce').dt.date

print('\n')
print(read_data['PO_date'].describe())
print('\n')
print('Data type:' ,type(read_data['PO_date']))
#read_data['PO_date'] = pd.to_datetime(read_data['PO_date'].map(datetime.date))
#read_data['PO_date'] = read_data['PO_date'].dt.strftime('%m/%d/%y')

#print(read_data['PO_date'])
print('\n')
print('Data dimension: ',read_data.shape)

#we use 6months of behavioural data(purchases) to predict first purchases in next 3 months
data_6m = read_data[(read_data.PO_date < date(2021,10,7)) 
    & (read_data.PO_date >= date(2021,4,1))].reset_index(drop=True)
#next 3months
data_next3m = read_data[(read_data.PO_date >= date(2021,10,7)) 
    & (read_data.PO_date < date(2022,3,1))].reset_index(drop=True)

print('\n')
print(data_next3m)
print('\n')
print(data_6m.columns.tolist())
#we will create a dataframe called data_user to possess a user level feature set for prediction level
data_user = pd.DataFrame(data_6m['CustomerID'].unique())
data_user.columns = ['CustomerID']
print(data_user)

#creating a dataframe with customerid and first purchase date in data_next3m
data_next_first_purchase = data_6m.groupby('CustomerID').PO_date.min().reset_index()
data_next_first_purchase.columns = ['CustomerID','First_Purchase_date']
"""print(data_next_first_purchase)"""

#create a data frame with customer id and last purchase date in 6 month
data_last_purchase = data_6m.groupby('CustomerID').PO_date.max().reset_index()
data_last_purchase.columns = ['CustomerID','Last_purchase_date']
'''print('\n')
print(data_last_purchase)'''
avg_purchase_rate = data_6m.groupby('CustomerID').PO_date.apply(lambda x:x.diff().dropna().mean())
avg_purchase_rate.columns = ['CustomerID','Purchase_Frequency']

'''print(avg_purchase_rate)'''
#mergin two dataframes
data_purchase_dates = pd.merge(data_next_first_purchase,data_last_purchase,on='CustomerID',how='left')

data = pd.merge(data_purchase_dates,avg_purchase_rate,on='CustomerID',how='left')
data.columns = ['CustomerID','First_Purchase','Last_purchase','Purchase_frequency']
print(data)
'''print(data_purchase_dates)'''

#creating a dataframe with customerid and first purchase date in data_next3m
data_next3m_first_purchase = data_next3m.groupby('CustomerID').PO_date.min().reset_index()
data_next3m_first_purchase.columns = ['CustomerID','First_Purchase_date_next3m']
print(data_next3m_first_purchase)

#create a data frame with customer id and last purchase date in 6 month
data_last_purchase = data_6m.groupby('CustomerID').PO_date.max().reset_index()
data_last_purchase.columns = ['CustomerID','Last_purchase_date']
#mergin two dataframes
data_purchase_dates1 = pd.merge(data_last_purchase,data_next3m_first_purchase,on='CustomerID',how='left')
data_purchase_dates1.columns = ['CustomerID','Last_purchase_date','first_purchase_date_next3m']

import datetime

data_purchase_dates1['Next_purchase_Day'] = (data_purchase_dates1['first_purchase_date_next3m'] - data_purchase_dates1['Last_purchase_date']).dt.days
data_purchase_dates1['Next_purchase_Day'] = pd.to_numeric(data_purchase_dates1['Next_purchase_Day'], downcast='integer')
data_purchase_dates1 = data_purchase_dates1.fillna(999)
#print(data_purchase_dates1['Next_purchase_Day'])
data_purchase_dates1['Next_purchase_date'] = (data_purchase_dates1['Last_purchase_date']) + pd.TimedeltaIndex(data_purchase_dates1['Next_purchase_Day'],unit='D')#.map(datetime.timedelta)

print(data_purchase_dates1)
 
 