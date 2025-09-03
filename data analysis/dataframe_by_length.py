import pandas as pd
import numpy as np
df = pd.read_csv('gita_translations_all.csv')
df['Length'] = df['Translation'].str.len()
#print(df)
avg_length=df['Length'].mean()
max_length=df['Length'].max()
min_length=df['Length'].min()
p1=np.mean([avg_length,max_length])
p2=np.mean([avg_length,min_length])
#size of verse categorization
df['size']=np.where(
    (df['Length']>=p1),
    "long"
    ,np.where(
        (df['Length']>=p2) & (df['Length']<p1),
        "medium",
        
        "short"
        
    )     
)
small_verses=df[df['Length']<p2]
medium_verses=df[(df['Length']>p2)& (df['Length']<p1)]
long_verses=df[df['Length']>p1]
