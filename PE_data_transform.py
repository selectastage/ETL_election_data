import pandas as pd
import random 


# Read output from scrape into dataframe
scrape_output = pd.read_csv('california_district_stats_src.csv')

## Data Cleaning

# Rename Columns
columns_to_rename_2 = ['White', 'Black', 'Native', 'Asian', 'Islander', 'Other', 'Two+', 'Hispanic']
columns_2_renamed_to = ['percent_ethnicity_' + i.lower() for i in columns_to_rename_2]

columns_to_rename_3 = ['Drove', 'Carpooled', 'Public', 'Bicycle', 'Walked']
columns_3_renamed_to = ['percent_mode_of_transport_' + i.lower() for i in columns_to_rename_3]

rename_dict_1 = zip(columns_to_rename_2, columns_2_renamed_to)
rename_dict_2 = zip(columns_to_rename_3, columns_3_renamed_to)

# Rename columns
scrape_output.rename(dict(rename_dict_1),axis = 1,inplace=True)
scrape_output.rename(dict(rename_dict_2),axis = 1, inplace=True)

# Type conversion

def type_conversion(dataframe):

    '''
    Method strips all string data points to prepare them for 
    type conversion with built-in Python function. All columns containing percent 
    are converted to decimals 

    return: None
    '''

    # capture the columns with percent values
    percentage_cols = [i for i in dataframe.columns if 'percent_' in i] + ['0-9','10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']

    # function to strip string values 
    trim_strings = lambda x: x.strip('$%† minutes').replace(',','') if isinstance(x, str) else x
    # function to make percentage conversion 
    percent_value = lambda x: float(x)/100

    # apply conversion to full dataframe
    dataframe = dataframe.applymap(trim_strings)
    dataframe[percentage_cols] = dataframe[percentage_cols].applymap(percent_value)

    return dataframe

scrape_output = type_conversion(scrape_output)

# Change & drop old variables
columns_to_replace = ['0-9','10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']

scrape_output['share_of_young_voters'] = scrape_output['0-9'] + scrape_output['10-19'] + scrape_output['20-29']
scrape_output['share_of_middle_aged_voters'] = scrape_output['30-39'] + scrape_output['40-49'] + scrape_output['50-59']
scrape_output['share_of_senior_voters'] = scrape_output['60-69'] + scrape_output['70-79'] + scrape_output['80+']

scrape_output = scrape_output.drop(columns = columns_to_replace)

# Introduce & resolve additional impurities

def create_missing(df, col_name: str):

    '''
    Method introduces 10 random inpurities of a different type 
    into a decimal Series in the dataframe. 

    return: None
    '''
    
    # add 10 random missing values
    random_ints = set(sorted([random.randint(1,len(df)) for i in range(0,10)]))

    for i in random_ints:
        df.loc[i-1, col_name] = 'NaN'

create_missing(scrape_output, 'share_of_young_voters')

# Introduce & resolve additional impurities

def fill_missing(df, col_name: str, other_cols: list):

    '''
    Finds missing NaN values in dataframe column and fills them based on adjacent percentage values
    specified in list of other columns.

    argument: Pandas dataframe, column name, other column names
    return: Pandas dataframe
    '''
 
    # find missing values
    for i in df[col_name].iteritems():
        if i[1] == 'NaN':
            # fill percentage share since the related columns have to add to 1 with other columns
            df.loc[i[0], col_name] = 1 - sum(df.loc[i[0], other_cols])

    return df

scrape_output = fill_missing(scrape_output, 'share_of_young_voters', other_cols=['share_of_senior_voters','share_of_middle_aged_voters'])

scrape_output.to_csv('california_district_stats_cleaned.csv', index = False)

print(scrape_output.head())

