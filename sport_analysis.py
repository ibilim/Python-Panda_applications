##My solutions to Sport Analysis
# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[1]:


import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[2]:


# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[2]:


def answer_one():
    gold=df.copy()
    gold['country']=gold.index
    gold=gold.set_index('Gold')
    gold=gold['country']
    return gold.loc[gold.index.max()]
answer_one()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[3]:


def answer_two():
    dif_gold=df.copy()
    dif_gold['Difference']=abs(dif_gold['Gold']-dif_gold['Gold.1'])
    dif_gold['country']=dif_gold.index
    dif_gold=dif_gold.set_index('Difference')
    dif_gold=dif_gold['country']
    return dif_gold.loc[dif_gold.index.max()]
answer_two()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[4]:


def answer_three():
    rg=df.copy()
    rg=rg[(rg['Gold']>0) & (rg['Gold.1']>0)] 
    rg['Relative']= abs(rg['Gold']-rg['Gold.1'])/(rg['Gold']+rg['Gold.1'])
    rg['country']=rg.index
    rg=rg.set_index('Relative')
    rg=rg['country']
    return rg.loc[rg.index.max()]
answer_three()


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.
# 
# *This function should return a Series named `Points` of length 146*

# In[16]:


def answer_four():
    gsb=df.copy()
    gsb['Points']=gsb['Gold.2']*3+ gsb['Silver.2']*2+gsb['Bronze.2']*1
    return gsb['Points']
answer_four()


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2015/co-est2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[6]:


census_df = pd.read_csv('census.csv')
census_df.head()


# In[7]:


def answer_five():
    census_df=pd.read_csv('census.csv')
    census_df=census_df.set_index('STNAME').sum(level='STNAME')
    return census_df['COUNTY'].idxmax()
answer_five()


# ### Question 6
# **Only looking at the three most populous counties for each state**, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

# In[14]:


def answer_six():
    pop3=pd.read_csv('census.csv')
    pop3=pop3[pop3['SUMLEV'] == 50]
    most3=pop3.sort_values('CENSUS2010POP', ascending=False).groupby('STNAME').head(3)
    return most3.groupby('STNAME').sum().sort_values('CENSUS2010POP', ascending=False).head(3).index.tolist()
answer_six()


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# In[9]:


def answer_seven():
    pop=pd.read_csv('census.csv')
    pop=pop[pop['SUMLEV']==50]
    pop=pop[['CTYNAME','POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012',
        'POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']].set_index('CTYNAME')
    for i in range(5):
        pop[str(i)+str(i+1)]=abs(pop[pop.columns[i]]- pop[pop.columns[i+1]])
    for i in range(4):
        pop[str(i)+str(i+2)]=abs(pop[pop.columns[i]]- pop[pop.columns[i+2]])
    for i in range(3):
        pop[str(i)+str(i+3)]=abs(pop[pop.columns[i]]- pop[pop.columns[i+3]])
    for i in range(2):
        pop[str(i)+str(i+4)]=abs(pop[pop.columns[i]]- pop[pop.columns[i+4]])
    for i in range(1):
        pop[str(i)+str(i+5)]=abs(pop[pop.columns[i]]- pop[pop.columns[i+5]])
    return pop[pop.columns[-15:]].idxmax().max()
answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[10]:


def answer_eight():
    pop=pd.read_csv('census.csv')
    df=pop.copy()
    for i in df.index:
        if str(df['CTYNAME'][i]).startswith('Washington')==False:
            df=df.drop(i)
    df=df[(df['REGION']<3) & (df['POPESTIMATE2015'] > df['POPESTIMATE2014'])]
    df=df[['STNAME', 'CTYNAME']]
    return df
answer_eight()


# In[ ]:





