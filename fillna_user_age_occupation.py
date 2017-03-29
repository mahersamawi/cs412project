import numpy
from scipy.stats import mode
import pandas as pd

user_df = pd.read_csv('inputs/user.txt')
#user_df['Gender'] = user_df['Gender'].fillna(mode(user_df['Gender'])[0][0])
user_df['Occupation'] = user_df['Occupation'].fillna(mode(user_df['Occupation'])[0][0])
user_df['Occupation'] = user_df['Occupation'].astype(int)
user_df['Age'] = user_df['Age'].fillna(numpy.mean(user_df['Age']))
user_df['Age'] = user_df['Age'].astype(int)

# I actually think it is easier to work directly with dataframe
# but I will convert it to file anyway...
user_df.to_csv('user_new.txt', index=False, na_rep='N/A')
