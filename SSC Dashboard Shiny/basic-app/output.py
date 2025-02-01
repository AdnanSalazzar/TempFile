from pathlib import Path
import pandas as pd

dir = Path(__file__).parent
df = pd.read_stata(dir / "SCS_data.dta")
# group_data = df.groupby('enumid')['allnoncontact'].sum().reset_index()

#outputdata = df[['enumid', 'allnoncontact', 'day']]

# group_data = df.groupby('enumid')['allnoncontact'].sum().reset_index()


# data = df.groupby('day').size().reset_index(name='count')
# print('hello')
# data = df[df['sex'] == 'Female'].shape[0]

data = df[['starttime' , 'endtime']].head(3)

print(data)