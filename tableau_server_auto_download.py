import os
from selenium import webdriver
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
from tabulate import tabulate
import itertools
import wget

start= time.time()

# Choose a Tableau Server version to download
wanted_version= '2021.2.1'

# Set default download directory
download_directory= r"D:\Users\test-user\test"

# Set options for Chrome driver
chrome_options= webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chromedriver_directory= r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
prefs = {"download.default_directory" : f"{download_directory}"}
chrome_options.add_experimental_option("prefs",prefs)

# Create a Chrome driver
driver = webdriver.Chrome (executable_path= chromedriver_directory, options= chrome_options)

# Download page for all version
ts_download_url = "https://www.tableau.com/support/releases/server"
driver.get(ts_download_url)

# Use xpath to find all download page element
all_download_page_elements= driver.find_elements_by_xpath('//a[@class="text--medium-body"]')

# Loop through the page elements to extract each download page and version string
all_download_page_list= []
all_version_list= []
for element in all_download_page_elements:
    download_page= element.get_attribute('href')
    version = os.path.basename(download_page)
    all_download_page_list.append(download_page)
    all_version_list.append(version)

# Loop through the download page list to extract download link
all_download_link_list= []
for download_page in all_download_page_list:
    driver.get(download_page)
    try:
        download_link_element= driver.find_element_by_xpath('//*[@id="esdalt"]/div/div[1]/ul/li[2]/a')
    except NoSuchElementException:
        download_link_element= None
    if download_link_element is not None:
        download_link= download_link_element.get_attribute('href')
        all_download_link_list.append(download_link)
    else:
        download_link= 'Not Available'
        all_download_link_list.append(download_link)

# Create a dataframe to store version, download page and download link
list_tuples = list(itertools.zip_longest(all_version_list, all_download_page_list, all_download_link_list))
df= pd.DataFrame(list_tuples, columns=['Version', 'Download Page', 'Download Link'])
print(tabulate(df, headers='keys', tablefmt='psql'))

# Download a Tableau version that match our wanted version
download_url= df.loc[df['Version']== wanted_version, 'Download Link'].iloc[0]
wget.download(download_url, download_directory)
print(f'"{os.path.basename(download_url)}" was successfully downloaded to "{download_directory}"')

# Close the driver
driver.quit()

end= time.time()
time_to_run= time.gmtime(end- start)
print("How long does it take to run this script:" , time.strftime("%H:%M:%S",time_to_run))

