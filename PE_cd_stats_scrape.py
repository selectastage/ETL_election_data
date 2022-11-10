# Module Imports

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

# Get URLS of interest

sub_10_urls = [f'https://censusreporter.org/profiles/50000US060{i}-congressional-district-0{i}-ca/' for i in range(1, 10)]  # first 10 congressional districts
rest_urls = [f'https://censusreporter.org/profiles/50000US06{i}-congressional-district-{i}-ca/' for i in range(10, 54)]  # remaining congressional districts
all_urls = sub_10_urls + rest_urls


# Restrict Browser UI launch upon URL access 

chrome_options = Options()
chrome_options.add_argument("--headless")

# Webscraping Class

class District_Stats:

    '''
    Class definition to intiliase Selenium driver. Class objects are defined using url. Elements on the scraped site are fetched with standard Xpath strings.
    '''

    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)

    def _return_element(self,xpath:str):
        
        '''
        Returns text from xpath element
        
        :argument xpath string for source code element
        :rtype: Selenium xpath element
        :return: string value contained in elements
        '''
        element = self.driver.find_element(by=By.XPATH, value=xpath).text
        return element

    def fetch_stats(self):

        '''
        Returns data in the standard Xpath elements and stores them in
        a single dictionary structure
        
        :return: statistics dictionary as per specified URL
        '''

        # Summary Stats
        
        s_a = {'population': self._return_element('//*[@id="cover-profile"]/article/div[1]/div/span/span[1]'),
               'people_per_square_mile': self._return_element('//*[@id="cover-profile"]/article/div[2]/div/span[2]/span[1]')}
               
        # Demographics
        dem_a = {'median_age': self._return_element('//*[@id="demographics"]/div/section[1]/div[1]/a/span/span[1]')}
        dem_b = {self._return_element(f'//*[@id="chart-histogram-demographics-age-distribution_by_decade-total"]/div/div[2]/a[{i}]').split()[1]: 
                 self._return_element(f'//*[@id="chart-histogram-demographics-age-distribution_by_decade-total"]/div/div[2]/a[{i}]').split()[0] for i in range(1, 10)}
        dem_c = {self._return_element(f'//*[@id="chart-column-demographics-race"]/div/div[2]/a[{i}]').split()[1]: 
                 self._return_element(f'//*[@id="chart-column-demographics-race"]/div/div[2]/a[{i}]').split()[0] for i in range(1, 9)}    

        # Economics
        econ_a  = {'per_capita_income': self._return_element(f'//*[@id="economics"]/div/section[1]/div[1]/a/span/span[1]')}                               
        econ_b =  {'median_household_income': self._return_element(f'//*[@id="economics"]/div/section[1]/div[2]/a/span/span[1]')}         
        econ_c =  {'percent_below_pov_per': self._return_element(f'//*[@id="economics"]/div/section[2]/div[1]/a/span/span[1]')}
        econ_d =  {'mean_commute_in_mins': self._return_element(f'//*[@id="economics"]/div/section[3]/div[1]/a/span/span[1]')}
        econ_e = {self._return_element(f'//*[@id="chart-histogram-economics-employment-transportation_distribution"]/div/div[2]/a[{i}]').split()[1]: 
                  self._return_element(f'//*[@id="chart-histogram-economics-employment-transportation_distribution"]/div/div[2]/a[{i}]').split()[0] for i in range(1, 7)}    
        				
        # Families
        fam_a =  {'house_count': self._return_element(f'//*[@id="families"]/div/section[1]/div[1]/a/span/span[1]')}
        fam_b =  {'pp_household': self._return_element(f'//*[@id="families"]/div/section[1]/div[2]/a/span/span[1]')}
        fam_c =  {'percent_mother_past_year': self._return_element(f'//*[@id="families"]/div/section[3]/div[1]/a/span/span[1]')} #split()[0]
                                           

        # Housing
        house_a =  {'housing_units': self._return_element(f'//*[@id="housing"]/div/section[1]/div[1]/a/span/span[1]')}
        house_b =  {'median_house_price': self._return_element(f'//*[@id="housing"]/div/section[3]/div[1]/a/span/span[1]')}

 
        # Education
        edu_a =  {'percent_high_school_education_or_higher': self._return_element(f'//*[@id="social"]/div/section[1]/div[1]/div[1]/a/span/span[1]').split()[0]}
        edu_b =  {'percent_secondary_education_or_higher': self._return_element(f'//*[@id="social"]/div/section[1]/div[1]/div[2]/a/span/span[1]').split()[0]}


        # Social
        soc_a = {'percent_foreign_language_speakers': self._return_element(f'//*[@id="social"]/div/section[2]/div[1]/a/span/span[1]').split()[0]}
        soc_b = {'percent_foreign_language_speakers': self._return_element(f'//*[@id="social"]/div/section[3]/div[1]/a/span/span[1]').split()[0]}
        
        variables = [s_a, dem_a, dem_b, dem_c, econ_a,econ_b, econ_c, econ_d, econ_e, fam_a, fam_b, fam_c, house_a, house_b, edu_a, edu_b,soc_a, soc_b]
        
        self.all_data_dict = dict()

        for i in variables:
            self.all_data_dict.update(i.items())

        return self.all_data_dict

    def create_data_frame(self):

        '''
        Leverages Pandas data frame class to return
        tabular structure from the statistics dictionary in the initiliased Class object.

        :return statistics data frame
        '''

        stat_lists = self.fetch_stats()

        # Create data frame using the url containing the congressional district number as the index
        df = pd.DataFrame(stat_lists, index=[int(self.url[-6:-4])])
        
        # Reset the index as the congressional district number
        df.reset_index(inplace=True)
        df = df.rename(columns={'index': 'Congressional District ID'})

        return df


# Create Dataframe

def create_final_out(urls:list):

    '''
    Iterates over provided URLs to instantiate data frames and concat output. 

    :argument: list of URLs / districts of interest
    :return: concatenated dataframe for all URLs / districts of interest
    '''
    
    all_values = []
    for i in urls: 
        district = District_Stats(url = i)
        # instantiate class Objects
        result = district.create_data_frame()
        all_values.append(result)
    
    # concatenate final data frame
    df_final = pd.concat(all_values)

    return df_final

# Create output
output = create_final_out(urls=all_urls)

# Create header of data frame
print(output.head())

# Extract final output
output.to_csv('california_district_stats_src_dirty.csv', index = False)
