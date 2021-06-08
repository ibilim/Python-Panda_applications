
##My own solutions to Hypothesis Testing
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[15]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[2]:


def get_list_of_university_towns():
    global uni_towns
    #states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    new_states={}
    #for i,k in states.items():
        #new_states[k]=i
    file=open('university_towns.txt')
    uni_towns=pd.DataFrame(columns=['State', 'RegionName'])
    for i in file:
        i=i.rstrip()
        if i.endswith('[edit]'): 
            state=i[:-6]
            #print(state)
        elif i.endswith(')') or i.endswith(']'):
            i=i.split()
            count=0
            for k in i:
                count=count+1
                if '(' in k:
                    break
            if count>0:
                town=' '.join(i[:i.index(k)])
            else:
                town=i[0]
            uni_towns=uni_towns.append(pd.DataFrame([[state,town]],columns=['State', 'RegionName']), ignore_index=True)
        else:
            i=i.split()
            try:
                town=' '.join(i[:i.index(k)])
            except:
                town=i[0]
            uni_towns=uni_towns.append(pd.DataFrame([[state,town]],columns=['State', 'RegionName']), ignore_index=True)
    #uni_towns['State']=uni_towns['State'].map(new_states)
    return uni_towns
get_list_of_university_towns()


# In[4]:


def get_recession_start():
    answers=list()
    recession=pd.read_excel('gdplev.xls',skiprows=220, header=None,usecols=[4,6]).rename(columns={4:'quarter',6:'GDP'})
    for i in range(len(recession['GDP'])-5):
        if recession.loc[i,'GDP']>recession.loc[i+1,'GDP'] and recession.loc[i+1,'GDP']>recession.loc[i+2,'GDP'] and recession.loc[i+2,'GDP']<recession.loc[i+3,'GDP'] and recession.loc[i+3,'GDP']<recession.loc[i+4,'GDP']:
            answers.append(recession.loc[i-1,'quarter'])
    return answers[0]
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
get_recession_start()


# In[7]:


def get_recession_end():
    answers=list()
    recession=pd.read_excel('gdplev.xls',skiprows=220, header=None,usecols=[4,6]).rename(columns={4:'quarter',6:'GDP'})
    for i in range(len(recession['GDP'])-5):
        if recession.loc[i,'GDP']>recession.loc[i+1,'GDP'] and recession.loc[i+1,'GDP']>recession.loc[i+2,'GDP'] and recession.loc[i+2,'GDP']<recession.loc[i+3,'GDP'] and recession.loc[i+3,'GDP']<recession.loc[i+4,'GDP']:
            answers.append(recession.loc[i+4,'quarter'])
    return answers[0]
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
get_recession_end()


# In[8]:


def get_recession_bottom():
    answers=list()
    recession=pd.read_excel('gdplev.xls',skiprows=220, header=None,usecols=[4,6]).rename(columns={4:'quarter',6:'GDP'})
    for i in range(len(recession['GDP'])-5):
        if recession.loc[i,'GDP']>recession.loc[i+1,'GDP'] and recession.loc[i+1,'GDP']>recession.loc[i+2,'GDP'] and recession.loc[i+2,'GDP']<recession.loc[i+3,'GDP'] and recession.loc[i+3,'GDP']<recession.loc[i+4,'GDP']:
            answers.append(recession.loc[i+2,'quarter'])
    return answers[0]
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
get_recession_bottom()


# In[9]:


def convert_housing_data_to_quarters():
    global housing_new
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    housing=pd.read_csv('City_Zhvi_AllHomes.csv',header=0)
    housing_new=pd.DataFrame(housing[['State', 'RegionName']])
    count=0
    for i in range(17):
        count=count+1
        housing_new[str(2000+i)+'q1']=(housing[str(2000+i)+'-01']+housing[str(2000+i)+'-02']+housing[str(2000+i)+'-03'])/3
        #housing_new[str(2000+i)+'q1']=housing_new[str(2000+i)+'q1'].astype('float')
        housing_new[str(2000+i)+'q2']=(housing[str(2000+i)+'-04']+housing[str(2000+i)+'-05']+housing[str(2000+i)+'-06'])/3
        #housing_new[str(2000+i)+'q2']=housing_new[str(2000+i)+'q1'].astype('float')
        if count==17:
            housing_new[str(2000+i)+'q3']=(housing[str(2000+i)+'-07']+housing[str(2000+i)+'-08'])/2
            #housing_new[str(2000+i)+'q3']=housing_new[str(2000+i)+'q1'].astype('float')
            break       
        housing_new[str(2000+i)+'q3']=(housing[str(2000+i)+'-07']+housing[str(2000+i)+'-08']+housing[str(2000+i)+'-09'])/3
        #housing_new[str(2000+i)+'q3']=housing_new[str(2000+i)+'q1'].astype('float')
        housing_new[str(2000+i)+'q4']=(housing[str(2000+i)+'-10']+housing[str(2000+i)+'-11']+housing[str(2000+i)+'-12'])/3
        #housing_new[str(2000+i)+'q4']=housing_new[str(2000+i)+'q1'].astype('float')
    housing_new['State']=housing_new['State'].map(states)
    housing_new=housing_new.set_index(['State','RegionName'])
    return housing_new
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.    '''
convert_housing_data_to_quarters()


# In[10]:


from scipy import stats
def run_ttest():
    global uni_towns,housing_new
    housing_new['Price_ratio']=housing_new['2008q3']/housing_new['2009q2']
    housing_new['groups']=np.nan
    uni_towns=uni_towns.set_index(['State', 'RegionName']).sort_index()
    housing_new=housing_new.sort_index()
    for i in housing_new.index:
        if i in uni_towns.index:
            housing_new.loc[i,'groups']= 'uni'
        else:
            housing_new.loc[i,'groups']= 'non_uni'
    non_uni_towns=housing_new[housing_new['groups']=='non_uni']
    uni_town=housing_new[housing_new['groups']=='uni']
    (statistic,p)=stats.ttest_ind(non_uni_towns['Price_ratio'],uni_town['Price_ratio'],nan_policy='omit')
    (different, p, better)=(None,p,None)
    if p<0.01: different=True
    else: different=False
    if non_uni_towns['Price_ratio'].mean()<uni_town['Price_ratio'].mean():better='non-university town'
    else: better='university town' 
    
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    return (different, p, better)

run_ttest()


# In[ ]:





# In[ ]:




