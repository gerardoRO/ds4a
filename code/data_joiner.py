import pandas as pd
import numpy as np

#Load all datasets
dataset_folder = 'datasets/'

pp_df = pd.read_csv(dataset_folder + 'cleaned_public_policy.csv')
inc1_df = pd.read_csv(dataset_folder + 'DS4AEDA2.csv')
inc2_df = pd.read_csv(dataset_folder + '06-12ds4a.csv')

#Adjust public policy data to match financial data
pp_df['Year'] = pd.to_datetime(pp_df['Year']).dt.year
pp_df = pp_df[pp_df['Year'] > 2006]

#Merge financial datasets
inc1_df.rename({'FIPS2010':'FIPS'},axis=1,inplace=True)
inc_tot_df = pd.concat([inc1_df, inc2_df])

#drop NaNs
inc_tot_df = inc_tot_df.dropna()

#Merge financial with public policy
df = pd.merge(pp_df,inc_tot_df,on=['State','Year'],how='inner')

#Adjusting FMR0 and Rent50 for bigger places, scaling from monthly to yearly
df['FMR0'] = df['FMR0'] * 1.36 *12
df['Rent50'] = df['Rent50'] * 1.36 *12

#Adjust prices for income
df['Income_Adjusted_FMR0'] = df['FMR0'] / df['MedianIncome']
df['Income_Adjusted_Rent50']  = df['Rent50']  / df['MedianIncome']
df['Income_Adjusted_HousingPrices']  = df['Housing_Prices_Quarter']  / df['MedianIncome']

#Identify afffordability
df['Affordability_Price_Point'] = df['MedianIncome'] * .3
df['Is_Rent_Affordable'] = df['Rent50'] < df['Affordability_Price_Point']
df['Is_FMR0_Affordable'] = df['FMR0'] < df['Affordability_Price_Point']

df['Truncated_FIPS'] = df['FIPS'].apply(lambda val: int(str(val)[0:6]))

df.drop(['Truncated_FIPS','FIPS'],axis=1,inplace=True)


## Testing mapping the categorical columns to true-false for easier interaction with Tableau

cat_cols = ['Private_Fair_Housing','No_Discrimination_Laws',
             'Public_Fair_Housing','Urban_Fair_Housing',
             'Banned_Discrimination_Public_Housing',
             'Banned_Discrimination_Private_Housing',
             'Legislation_Public_Housing','Rent_Control',
             'State_Aid_Allowed','Federal_Aid_Allowed','Prohibit_Rent_Control']
for col in cat_cols:
    print(f'Unique cols in {col}: ' + str(df[col].unique()))
    df[col] = df[col].map({0.:False,1.0:True,2.0:True,10.0:True})
    print(f'Unique cols in {col}: ' + str(df[col].unique()))
        
df['Metro'] = df['Metro'].map({1:True,0:False})        
df.to_csv(dataset_folder +'current_final_datset.csv',index =False)