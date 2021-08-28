import os
from selenium import webdriver
import pandas as pd
import time
from tabulate import tabulate
import wget
import itertools
from selenium.webdriver.support.ui import Select

start= time.time()

# Choose the year to download data
wanted_year= list(range(2019, 2021, 1)) # end year must be +1. For example, if we want 2018-2020, then range(2018,2021,1)

# Set default download directory
download_directory= r"D:\Users\znguyen\test"

# Set IPEDS base URL
base_url = "https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx?goToReportId=7"

# Set options for Chrome driver
chrome_options= webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chromedriver_directory= r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
prefs = {"download.default_directory" : f"{download_directory}"}
chrome_options.add_experimental_option("prefs",prefs)

# Create a Chrome driver
driver = webdriver.Chrome (executable_path= chromedriver_directory, options= chrome_options)

# Go to the IPEDS base url
driver.get(base_url)

# Find the select year and select survey drop-down menu
select_year = Select(driver.find_element_by_xpath('//select[@id="contentPlaceHolder_ddlYears"]'))
select_survey= Select(driver.find_element_by_xpath('//select[@id="ddlSurveys"]'))

# Select option "all year" and "all survey" from the drop-down menu
all_year= select_year.first_selected_option
all_survey= select_survey.first_selected_option

# Click on the Continue button
driver.find_element_by_xpath('//*[@id="contentPlaceHolder_ibtnContinue"]').click()

## BUILD A DATAFRAME CONTAINS "YEAR, SURVEY, TITLE, DATA DOWNLOAD LINK, DICTIONARY LINK"

# Get all data download link
all_download_elements= driver.find_elements_by_xpath('//*[@id="contentPlaceHolder_tblResult"]/tbody/tr/td[4]/a')
all_download_list= []
for element in all_download_elements:
    all_download_list.append(element.get_attribute('href'))

# Get all dictionaries download link
all_dictionary_elements= driver.find_elements_by_xpath('//*[@id="contentPlaceHolder_tblResult"]/tbody/tr/td[7]/a')
all_dictionary_list= []
for element in all_dictionary_elements:
    all_dictionary_list.append(element.get_attribute('href'))

# Get all YEAR, SURVEY, TITLE
all_year_elements= driver.find_elements_by_xpath('//*[@id="contentPlaceHolder_tblResult"]/tbody/tr/td[1]')
all_survey_elements= driver.find_elements_by_xpath('//*[@id="contentPlaceHolder_tblResult"]/tbody/tr/td[2]')
all_title_elements= driver.find_elements_by_xpath('//*[@id="contentPlaceHolder_tblResult"]/tbody/tr/td[3]')
all_year_list= []
all_survey_list= []
all_title_list= []
for element in all_year_elements:
    all_year_list.append(element.text)
for element in all_survey_elements:
    all_survey_list.append(element.text)
for element in all_title_elements:
    all_title_list.append(element.text)

# Create a dataframe contains 5 columns: "YEAR, SURVEY, TITLE, DATA DOWNLOAD LINK, DICTIONARY LINK"
list_tuples = list(itertools.zip_longest(all_year_list, all_survey_list, all_title_list, all_download_list, all_dictionary_list))
df= pd.DataFrame(list_tuples, columns=['Year', 'Survey', 'Title', 'Download Link', 'Dictionary Link'])
df['Year']= df['Year'].astype('float').astype('Int64')
print(tabulate(df, headers='keys', tablefmt='psql'))


# Download all surveys that match our wanted year
download_link_list= set(df['Download Link'].loc[df['Year'].isin(wanted_year)]) # use set to prevent duplicated link. For example, there are several FLAGS2019 or FLAGS2020
for download_link in download_link_list:
    wget.download(download_link, download_directory)
    print(f'"{os.path.basename(download_link)}" was successfully downloaded to "{download_directory}"')

# Close the driver
driver.quit()

end= time.time()
time_to_run= time.gmtime(end- start)
print("How long does it take to run this script:" , time.strftime("%H:%M:%S",time_to_run))