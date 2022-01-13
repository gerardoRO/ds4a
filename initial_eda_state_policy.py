import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('State_public policy.csv',low_memory = False)

interesting_columns = ['st','year','regulation_rent_control',
                       'frent','landfree','regulation_rent_control',
                       'housing_prices_quar','ahcdpi','ahcdpia',
                       'ahcdspt','ig_cons','ndl_housing'
                       'fhpriv','fhpub','fhurb','race_boehmke_fhpub',
                       'w_race_fair_housing_private','pubhouen',
                       'regulation_housing_directstate ai',
                       'regulation_housing_enabling_federal_aid',]


df.drop(df.columns.difference(interesting_columns),1,inplace=True) #remove excess data
df.dropna(axis = 0 , inplace = True) #remove na values

num_entries_state = df.groupby(['st'])


