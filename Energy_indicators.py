
##My own solutions to Energy Indicators Assignment

# # Assignment 3 - Energy Indicators
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[9]:


import pandas as pd
import numpy as np
def answer_one():
    global GDP, ScimEn,ScimE, energy, merge_2
    energy=pd.read_excel('Energy Indicators.xls',header=None,skiprows=18, skipfooter=38,usecols=[2,3,4,5]).rename(columns={2:'Country', 3:'Energy Supply',4:'Energy Supply per Capita',5:'% Renewable'})
    for i in range(len(energy)):
        if  str(energy.loc[i,'Energy Supply']).isnumeric(): energy.loc[i,'Energy Supply']*=1000000
        else: energy.loc[i,'Energy Supply']=np.nan
        if str(energy.loc[i,'Energy Supply per Capita'])=='...':energy.loc[i,'Energy Supply per Capita']=np.nan
        if str(energy.loc[i,'% Renewable'])=='...':energy.loc[i,'% Renewable']=np.nan
        if energy.loc[i,'Country'].endswith(')'): energy.loc[i,'Country']=energy.loc[i,'Country'].split()[0]
        if list(energy.loc[i,'Country'])[-1].isnumeric():
            new_name=list(energy.loc[i,'Country'])
            for n in new_name:
                if str(n).isnumeric(): 
                    new_name=new_name[:-1]
                    continue
            energy.loc[i,'Country']=''.join(new_name)
        if energy.loc[i,'Country']=='Republic of Korea': energy.loc[i,'Country']="South Korea"
        if energy.loc[i,'Country']=="United States of America": energy.loc[i,'Country']="United States"
        if energy.loc[i,'Country']=="United Kingdom of Great Britain and Northern Ireland":energy.loc[i,'Country']='United Kingdom'
        if energy.loc[i,'Country']=="China, Hong Kong Special Administrative Region":energy.loc[i,'Country']='Hong Kong'
    GDP=pd.read_csv('world_bank.csv',skiprows=4,header=0).rename(columns={'Country Name':'Country'})
    for i in range(len(GDP['Country'])):
        if GDP.loc[i,'Country']=='Korea, Rep.': GDP.loc[i,'Country']='South Korea'
        if GDP.loc[i,'Country']=='Iran, Islamic Rep.': GDP.loc[i,'Country']='Iran'
        if GDP.loc[i,'Country']=='Hong Kong SAR, China': GDP.loc[i,'Country']='Hong Kong'
    GDP=GDP[['Country','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    ScimE=pd.read_excel('scimagojr-3.xlsx')
    ScimEn=ScimE.head(15)
    energy['Energy Supply']=energy['Energy Supply'].astype('float64')
    energy['Energy Supply per Capita']=energy['Energy Supply per Capita'].astype('float64')
    merge_1=pd.merge(ScimEn, energy, how='inner', left_on='Country', right_on='Country')
    merge_2=pd.merge(merge_1, GDP, how='inner', left_on='Country', right_on='Country' ).set_index('Country')
    return merge_2
answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[2]:


get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[78]:


def answer_two():
    import pandas as pd
    import numpy as np
    mergall_1=pd.merge(ScimE, energy, how='outer', left_on='Country', right_on='Country',copy=False)
    mergall_2=pd.merge(mergall_1, GDP, how='outer', left_on='Country', right_on='Country',copy=False).set_index('Country')
    print( mergall_1)
    return len(mergall_2.drop(merge_2.index)), len(mergall_1)
answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[11]:


def answer_three():
    import pandas as pd
    import numpy as np
    merge_2['avgGDP']=merge_2[[ '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].mean(axis=1,skipna=True)
    return merge_2['avgGDP'].sort_values(ascending=False) #.apply(lambda x: '%.3f' % x)
answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[12]:


def answer_four():
    import pandas as pd
    import numpy as np
    merge_2['change10years']=merge_2['2015']-merge_2['2006']
    return merge_2.loc[str(merge_2['avgGDP'].sort_values(ascending=False).index[5]),'change10years']
answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[13]:


def answer_five():
    import pandas as pd
    import numpy as np
    return merge_2['Energy Supply per Capita'].mean()
answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[14]:


def answer_six():
    import pandas as pd
    import numpy as np
    for i,j in merge_2['% Renewable'].sort_values(ascending=False).head(1).items():
        return (i,j)
answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[15]:


def answer_seven():
    import pandas as pd
    import numpy as np
    merge_2['Self/Total']=merge_2['Self-citations']/merge_2['Citations']
    for i, j in merge_2['Self/Total'].sort_values(ascending=False).head(1).items():
        return (i,j)
answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[16]:


def answer_eight():
    import pandas as pd
    import numpy as np
    merge_2['Pop_est']=merge_2['Energy Supply']/merge_2['Energy Supply per Capita']
    return merge_2['Pop_est'].sort_values(ascending=False).index[2]
answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[17]:


def answer_nine():
    merge_2['Citable docs per Capita']=(merge_2['Citable documents']/merge_2['Pop_est']).apply(lambda x:'%.7f'%x)
    return merge_2['Citable docs per Capita'].astype('float').corr(merge_2['Energy Supply per Capita'].astype('int'))
answer_nine()


# In[14]:



def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    merge_2['Pop_est'] = merge_2['Energy Supply'] / merge_2['Energy Supply per Capita']
    merge_2['Citable docs per Capita'] = merge_2['Citable documents'] / merge_2['Pop_est']
    merge_2.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])
#plot9()


# In[ ]:


#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[53]:


def answer_ten():
    merge_2['HighRenew']=""
    for i in range(len(merge_2['% Renewable'])):
        if merge_2.loc[merge_2.index[i],'% Renewable'] >= merge_2['% Renewable'].median(axis=0):
            merge_2.loc[merge_2.index[i],'HighRenew']=1
        else:
            merge_2.loc[merge_2.index[i],'HighRenew']=0
    return merge_2['HighRenew'].astype('int64').sort_index()
answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[57]:


def answer_eleven():
    merge_2['Continent']=pd.Series({'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'})
    merge_2['Pop_est']=merge_2['Pop_est'].astype('float')
    continents=pd.DataFrame( columns=['size','sum','mean','std'],index=['Asia', 'Australia', 'Europe', 'North America', 'South America'])
    continents['mean']=merge_2.groupby('Continent').agg({'Pop_est':np.mean})
    continents['std']=merge_2.groupby('Continent').agg({'Pop_est':np.std})
    continents['sum']=merge_2.groupby('Continent').agg({'Pop_est':np.sum})
    continents['size']=merge_2.reset_index().set_index('Continent').groupby(level=0).agg({'Country':np.size}).astype('float64')
    return continents
answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[63]:


def answer_twelve():
    merge_2['Categories']=pd.cut(merge_2['% Renewable'],5)
    return merge_2.reset_index().set_index(['Continent','Categories'])['Country'].groupby(['Continent','Categories']) #.apply(np.size).dropna()
#answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[52]:


def answer_thirteen():
    global merge_2
    merge_2=merge_2.reset_index().set_index('Country')
    merge_2['PopEst']=merge_2['Pop_est'].apply(lambda x:'{:,}'.format(x))
    return  merge_2['PopEst']
answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[18]:



def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    ax = merge_2.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*merge_2['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(merge_2.index):
        ax.annotate(txt, [merge_2['Rank'][i], merge_2['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")

#plot_optional() 


#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!

