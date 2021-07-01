import pandas as pd
pd.options.display.width=None
pd.options.mode.chained_assignment = None
import glob
import re
import time
import os
import boto3

start= time.time() # set a start point to measure the elapsed time it take to run script

### NOTE: CHANGE THE INPUT and OUTPUT directory at line 15, 21 as well as the path to the data dictionary at line 18

# Path to the folder that contains raw data (Raw Data Files)
input_path = r'D:\Users\sample_user\CollegeScorecard_Raw_Data_01192021\Raw Data Files'

# Path to the data dictionary (the data dictionary would be downloaded separately, not in the raw data Zip file)
path_to_data_dictionary= r'D:\Users\sample_user\CollegeScorecard_Raw_Data_01192021\collegescorecarddatadictionary_2021-04-01.xlsx'

# Create a folder named "Cleaned Data Files" to store output files
output_path= r'D:\Users\sample\CollegeScorecard_Raw_Data_01192021\Cleaned Data Files'
if not os.path.exists(output_path):
    os.mkdir(output_path)

# Create files list for FieldOfStudyData (data by field of study) and MERGED data (data by institution_level)
field_of_study_files = glob.glob(input_path + r'\FieldOfStudyData*.csv')
institution_level_files= glob.glob(input_path + r'\MERGED*.csv')



## Read all the "FieldOfStudy" files (data by field of study) and concat into one data frame
field_of_study_list = [] # create an empty list to store all field of study data frame

for filename in field_of_study_files:
    temp_df = pd.read_csv(filename, low_memory= False, index_col= False,
                          dtype= {'UNITID': str, 'OPEID6': str, 'CIPCODE': str})

    # replace string "NULL" and string "PrivacySuppressed" with NA (pandas.NA)
    temp_df.replace(['NULL', 'PrivacySuppressed'], pd.NA, inplace=True)

    # fill all missing values with NA
    #temp_df.fillna(pd.NA, inplace= True)

    # convert OPEID6 to string and pad with ‘0’ characters on the left of the string to reach 6 digits
    #temp_df['OPEID6'] = temp_df['OPEID6'].str.zfill(6)

    # convert CIPCODE to string and pad with ‘0’ characters on the left of the string to reach 4 digits
    #temp_df['CIPCODE'] = temp_df['CIPCODE'].str.zfill(4)

    # create an indicator column named "ACAD_YR" to identify where rows originate from
    temp_df['ACAD_YR'] = re.findall(r'\d+_\d+', filename)[0]

    # shift column 'ACAD_YR' to first position
    first_column = temp_df.pop('ACAD_YR')
    temp_df.insert(0, 'ACAD_YR', first_column)

    # append all temp_df into one list
    field_of_study_list.append(temp_df)

# Concat 3 data frames into one data frame "field_of_study_data"
field_of_study_data = pd.concat(field_of_study_list, axis=0, ignore_index=True)

# Write to a csv file
field_of_study_data.to_csv(f'{output_path}/field_of_study_data.csv',
                           index= False, header= True)



## Read all the "MERGED" files (data by institution level) and concat into one data frame
institution_level_list = [] # create an empty list to store all institution level data frame

for filename in institution_level_files:
    temp_df = pd.read_csv(filename, low_memory= False, index_col= False,
                          dtype= {'UNITID': str, 'OPEID': str, 'OPEID6': str, 'ZIP': str})
    # replace string "NULL" and string "PrivacySuppressed" with NA (pandas.NA)
    temp_df.replace(['NULL', 'PrivacySuppressed'], pd.NA, inplace=True)

    # fill all missing values with NA
    #temp_df.fillna(pd.NA, inplace= True)

    # convert OPEID to string and pad with ‘0’ characters on the left of the string to reach 8 digits
    #temp_df['OPEID'] = temp_df['OPEID'].str.zfill(8)

    # convert OPEID6 to string and pad with ‘0’ characters on the left of the string to reach 6 digits
    #temp_df['OPEID6'] = temp_df['OPEID6'].str.zfill(6)

    # convert ZIP code to string, truncate 9 digits ZIP code to 5 digits, pad with ‘0’ to reach 5 digits
    #temp_df['ZIP'] = temp_df['ZIP'].astype(str).str.slice(0, 5)
    #temp_df['ZIP'] = temp_df['ZIP'].astype(str).str.zfill(5)

    # create an indicator column named "ACAD_YR" to identify where rows originate from
    temp_df['ACAD_YR'] = re.findall(r'\d+_\d+', filename)[0]

    # shift column 'ACAD_YR' to first position
    first_column = temp_df.pop('ACAD_YR')
    temp_df.insert(0, 'ACAD_YR', first_column)

    # append all temp_df into one list
    institution_level_list.append(temp_df)

# Concat 23 data frames into one data frame "institution_level_data"
institution_level_data = pd.concat(institution_level_list, axis=0, ignore_index=True)

# Split the "institution_level_data" into 10 data frames because the number of columns exceed Redshift limit 1600 columns
# Columns will be split based on the "dev-category" in the data dictionary
institution_data_dictionary= pd.read_excel(path_to_data_dictionary, sheet_name= 'institution_data_dictionary', engine= 'openpyxl')

# Forward fill to prevent error below since the data dictionary has special structure format
# ValueError: Cannot mask with non-boolean array containing NA / NaN values
institution_data_dictionary['VARIABLE NAME']= institution_data_dictionary['VARIABLE NAME'].fillna(method= 'ffill')

# Replace 4 mis-spelled "VARIABLE NAME" to prevent error below
# KeyError: "['D150_4_AIANOld', 'D150_L4_AIANOld', 'D150_4_HISPOld', 'D150_L4_HISPOld'] not in index"
institution_data_dictionary['VARIABLE NAME']= institution_data_dictionary['VARIABLE NAME'].str.upper()

# Group "VARIABLE NAME" by "dev-category", keep only unique "VARIABLE NAME"
variable_in_each_category= institution_data_dictionary.groupby('dev-category')['VARIABLE NAME'].unique()

# Split the "institution_level_data" into 10 data frames based on 10 "dev-category"
for category in range(len(variable_in_each_category)):
    subset_data= institution_level_data[variable_in_each_category[category]]

    # Keep the "ACAD_YR" and "UNITID" columns from the original data set for each of the subset data
    subset_data['ACAD_YR']= institution_level_data.loc[:, 'ACAD_YR']
    subset_data['UNITID']= institution_level_data.loc[:, 'UNITID']

    # Move these two columns to the first and second position for JOINING purpose
    first_column= subset_data.pop('ACAD_YR')
    second_column= subset_data.pop('UNITID')
    subset_data.insert(0, 'ACAD_YR', first_column)
    subset_data.insert(1, 'UNITID', second_column)

    # Create a variable to store category name
    category_name= variable_in_each_category.reset_index()['dev-category'][category]

    # Un-comment 2 lines below if you want to see what is in each subset_data
    #print(category_name)
    #print(subset_data)

    # Write to 10 csv files
    subset_data.to_csv(f'{output_path}/institution_level_data_{category_name}.csv', index=False, header=True)



## Import all files in output_path ("Cleaned Data Files" folder) to AWS S3
s3_bucket= "sample_bucket" # change the bucket name
profile_name= "sample_profile" # change the profile name

# Create a function to upload all files in a directory to a S3 bucket
def upload_files_to_s3(path):
    boto_sess = boto3.Session(profile_name= profile_name)
    s3 = boto_sess.resource('s3')
    bucket = s3.Bucket(s3_bucket)

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object(Key=full_path[len(path) + 1:], Body=data)

upload_files_to_s3(f'{output_path}')



## Check how much time it took to run this script
end= time.time() # set an end point to measure the elapsed time it took to run script
time_to_run= time.gmtime(end- start) # time to run the script in seconds
print("How long does it take to run this script:" , time.strftime("%H:%M:%S",time_to_run))
