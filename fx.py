import pandas as pd
from datetime import datetime, date 
import warnings
warnings.filterwarnings('ignore')

#reading the data
read_data = pd.read_csv('data.csv',skiprows=1,sep = ',')

print('The columns are: ')
print(read_data.columns.tolist())

#converting the date field from string to datetime
read_data['PO_date'] = pd.to_datetime(read_data['PO_date'],errors='coerce').dt.date

print('\n')
print(read_data['PO_date'].describe())
print('\n')
print('Data type:' ,type(read_data['PO_date']))
print('\n')
print('Data dimension: ',read_data.shape)

#we use 6months of behavioural data(purchases) to predict first purchases in next 3 months
data_6m = read_data[(read_data.PO_date < date(2021,10,7)) 
    & (read_data.PO_date >= date(2021,4,1))].reset_index(drop=True)
#next 3months
data_next3m = read_data[(read_data.PO_date >= date(2021,10,7)) 
    & (read_data.PO_date < date(2022,3,1))].reset_index(drop=True)

#we will create a dataframe for our customers
data_user = pd.DataFrame(data_6m['CustomerID'].unique())
data_user.columns = ['CustomerID']
print(data_user)

pd.set_option('display.max_rows',None,'display.max_columns',None,)

#creating a dataframe with customerid and first purchase date in 6month
data_first_purchase = data_6m.groupby('CustomerID').PO_date.min().reset_index()
data_first_purchase.columns = ['CustomerID','First_Purchase_date6m']
print('\nCustomers First purchase in 6 month')
print(data_first_purchase)

#create a data frame with customer id and last purchase date in 6 month    
data_last_purchase = data_6m.groupby('CustomerID').PO_date.max().reset_index()
data_last_purchase.columns = ['CustomerID','Last_purchase_date6m']
print('\nCusomter and their last purchase date in 6month')
print(data_last_purchase)

#finding the frequency of the purchase
avg_purchase_rate = data_6m.groupby('CustomerID').PO_date.apply(lambda x:x.diff().dropna().mean())
avg_purchase_rate.columns = ['CustomerID','Purchase_frequency6m']
print('\nCustomer and their frequency of purchase in 6 month')
print(avg_purchase_rate)

#mergin two dataframes: the last purchase from 6month and first purchase in next 6 month
data_purchase_dates = pd.merge(data_first_purchase,data_last_purchase,on='CustomerID',how='left')
#now merging the data purchase date with avg_purchase date
data = pd.merge(data_purchase_dates,avg_purchase_rate,on='CustomerID',how='left')
data.columns = ['CustomerID','First_Purchase6m','Last_purchase6m','Purchase_frequency6m']
'''data['Next_purchase_date'] = (data['Last_purchase6m']) + pd.Timedelta(days = data['Purchase_frequency6m'])'''
 
data['Purchase_frequency6m'] = pd.to_numeric(data['Purchase_frequency6m'], downcast='integer')
print(data['Purchase_frequency6m'])
'''data['Next_purchase_date'] = (data['Last_purchase6m']) + pd.TimedeltaIndex(data['Purchase_frequency6m'],unit='D')#.map(datetime.timedelta)
'''
print('\nCustomers with their first purchase ,last purchase & their frequency of purchase in 6month')
print(data)