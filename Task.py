# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 00:00:36 2021

@author: Ahmad Hossny
"""

#import urllib
import urllib.request
import pandas as pd
from io import StringIO
import ast
import json
import datetime as dt
from dateutil.relativedelta import relativedelta

data_url = 'https://data.gov.au/data/api/3/action/datastore_search?resource_id=809c77d8-fd68-4a2c-806f-c63d64e69842&limit=100000'  
            

with urllib.request.urlopen(data_url) as url:
    fileobj = url.read()
    #print (fileobj)


dict_str = fileobj.decode("UTF-8")
data_dict = json.loads(dict_str)
recs = data_dict['result']['records']
df = pd.DataFrame(recs)
print(df.shape)

df['Year']=pd.to_numeric(df['Year'])
df['Month_num']=pd.to_numeric(df['Month_num'])
df['Passengers_In']=pd.to_numeric(df['Passengers_In'])
df['Mail_In_(tonnes)']=pd.to_numeric(df['Mail_In_(tonnes)'])
df['Mail_Out_(tonnes)']=pd.to_numeric(df['Mail_Out_(tonnes)'])
df['Freight_In_(tonnes)']=pd.to_numeric(df['Freight_In_(tonnes)'])

# Question1
df2 = df.loc[df.Year==2019]
df3 = df2.groupby(['Airline', 'Month_num'])['Passengers_In','Passengers_Out'].apply(lambda x : x.astype(int).sum()).reset_index()

print(df3)
df3.to_csv('Answer_1.csv',index=False)

############################################

# Question2 
past_6_months_date = (dt.date.today() - relativedelta(months=6))

df4 = df.loc[(((df.Year>=past_6_months_date.year) & (df.Month_num>=past_6_months_date.month)) | ((df.Year==dt.date.today().year) & (df.Month_num<=dt.date.today().month)))].reset_index()
rec_idx = df4['Passengers_In'].values.argmax()

print ("Port_coutry with maximum passenger_in in past 6 months")
print(df4.iloc[rec_idx]['Port_Country'])

print(df4)
df4.to_csv('Answer_2.csv',index=False)
#######################################
#Question 3

df5 = df.loc[df.Year==2018]
df6 = df5.sort_values(['Airline','Year','Month_num'])
df7 = df6.groupby(['Airline']).rolling(window=3)['Freight_In_(tonnes)'].mean().reset_index()

print(df7)
df7.to_csv('Answer_3.csv',index=False)
#######################################
#Question 4

df8 = df.groupby(['Airline'])['Mail_In_(tonnes)','Mail_Out_(tonnes)'].agg('sum').reset_index()
df8 = df8[df8['Mail_Out_(tonnes)']>0]
df8 = df8.sort_values(['Airline'])
df8['mail_ratio'] = df8['Mail_In_(tonnes)']/df8['Mail_Out_(tonnes)'] 
df9 = df8.sort_values(['mail_ratio','Airline'], ascending = False)[:3]

print(df9)
df9.to_csv('Answer_4.csv',index=False)
#########################################
# Question 5

df10 = df.groupby(['Airline'])['Year'].agg('max').reset_index()
df10 .columns  =['Airline', 'Max_Year']
df11 = df.groupby(['Airline'])['Year'].agg('min').reset_index()
df11 .columns  =['Airline', 'Min_Year']
df12 = pd.merge(df10, df11, left_on='Max_Year', right_on='Min_Year', how='inner')

print(df12)
df12.to_csv('Answer_5.csv',index=False)


          




