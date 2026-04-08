import pandas as pd
df = pd.read_csv('data/credit_data.csv')
print(df['Class'].value_counts())